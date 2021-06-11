import json
import re
from Acquisition import aq_inner
from Acquisition import aq_parent
from zExceptions import Unauthorized
from zope import component
from zope.component import getUtility
from zope.interface import implements, Interface
from Products.PythonScripts.standard import url_quote
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IFolderish
from Products.ResourceRegistries.tools.packer import JavascriptPacker
from plone import api
from plone.portlets.interfaces import IPortletAssignment
from plone.registry.interfaces import IRegistry
from plone.app.portlets.browser.interfaces import IPortletAdding
from collective.ckeditor import LOG
from collective.ckeditor.config import CKEDITOR_PLONE_DEFAULT_TOOLBAR
from collective.ckeditor.config import CKEDITOR_BASIC_TOOLBAR
from collective.ckeditor.config import CKEDITOR_FULL_TOOLBAR
from collective.ckeditor.config import CKEDITOR_SUPPORTED_LANGUAGE_CODES
from collective.ckeditor import siteMessageFactory as _


import demjson
demjson.dumps = demjson.encode
demjson.loads = demjson.decode

CK_VARS_TEMPLATE = """
// set the good base path for the editor because
// portal_javascripts loose it
// otherwise ckeditor linked urls are bad
// important : this script must be called before ckeditor.js

var CKEDITOR_BASEPATH = '%(portal_url)s/++resource++ckeditor/';
var CKEDITOR_PLONE_BASEPATH = '%(portal_url)s/++resource++ckeditor_for_plone/';
var CKEDITOR_PLONE_PORTALPATH = '%(portal_url)s';
"""

ABSOLUTE_URL = re.compile("^https?://")


class ICKeditorView(Interface):
    """
    CKeditor browser view interface
    """


class CKeditorView(BrowserView):
    """
    CKeditor browser view
    """
    implements(ICKeditorView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal = getToolByName(
            self.context, 'portal_url').getPortalObject()
        self.portal_url = self.portal.absolute_url()
        request.set('ckLoaded', True)

    @property
    def cke_properties(self):
        pp = getToolByName(self.portal, 'portal_properties')
        return pp.ckeditor_properties

    @property
    def cke_properties_overloaded(self):
        return self.cke_properties.getProperty('properties_overloaded', [])

    def cke_config_url(self, context=None):
        """"
        return the dynamic configuration file url
        """

        def findContentish(context):
            # find context by walking up acquisition chain
            while True:
                context = aq_parent(context)
                if IContentish.providedBy(context):
                    break
                elif IFolderish.providedBy(context):
                    break
            return context

        # when used by plone.app.form.widgets.wysiwygwidget
        # to add or edit a portlet
        if IPortletAssignment.providedBy(context):
            context = findContentish(context)
        elif IPortletAdding.providedBy(context):
            context = findContentish(context)
        else:
            context = aq_inner(self.context)
        return '%s/ckeditor_plone_config.js' % context.absolute_url()

    @property
    def cke_basehref(self):
        """
        return the base href used by ckeditor
        to calculate relative or absolute links
        during edition (when copy pasting urls)
        by default it's the actual url
        """
        request = self.request
        return "%s" % request['ACTUAL_URL']

    @property
    def cke_language(self):
        """
        return language in content context
        """
        pstate = component.getMultiAdapter((self.context, self.request),
                                           name="plone_portal_state")
        return pstate.language()

    @property
    def cke_result_basehref(self):
        """
        return the base href
        used to calculate relative or absolute links
        after edition
        by default it's the global renderBase value
        """
        context = aq_inner(self.context)
        plone_view = context.restrictedTraverse('@@plone')
        return "'%s'" % plone_view.renderBase()

    @ property
    def ckfinder_basehref(self):
        """
        return CK finder base href
        TODO : improve it with control panel
        (could be a specific place in site)
        """
        context = aq_inner(self.context)
        return context.absolute_url()

    def _memberUsesCKeditor(self):
        """return True if member uses CKeditor"""
        pm = getToolByName(self.portal, 'portal_membership')
        member = pm.getAuthenticatedMember()
        editor = member.getProperty('wysiwyg_editor')
        if editor == 'CKeditor':
            return True
        if editor != '':
            return False
        # The member wants the default editor of the site.
        pprops = getToolByName(self.portal, 'portal_properties')
        editor = pprops.site_properties.getProperty('default_editor')
        return editor == 'CKeditor'

    def contentUsesCKeditor(self, fieldname=''):
        """
        return True if content uses CKeditor
        """
        context = aq_inner(self.context)
        request = self.request
        if self. _memberUsesCKeditor():
            if not fieldname:
                return True
            if not hasattr(context, 'getField'):
                return True
            field = context.getField(fieldname)
            if not field:
                return True
            text_format = request.get('%s_text_format' %
                                      fieldname,
                                      context.getContentType(fieldname))
            content = field.getEditAccessor(context)()
            try:
                if content.startswith('<!--'):
                    return False
            except:
                return False
            return 'html' in text_format.lower()
        return False

    def getCK_contentsCss(self):
        """
        return list of style sheets applied to ckeditor area
        the list is returned as a javascript string
        by default portal_css mixin + plone_ckeditor_area.css
        TODO : improve it with a control panel
        """
        context = aq_inner(self.context)
        portal = self.portal
        portal_url = self.portal_url
        portal_css = getToolByName(portal, 'portal_css')
        css_jsList = "["
        current_skin = context.getCurrentSkinName()
        skinname = url_quote(current_skin)
        css_res = portal_css.getEvaluatedResources(context)
        for css in css_res:
            media = css.getMedia()
            rel = css.getRel()
            if media not in ('print', 'projection') and rel == 'stylesheet':
                cssPloneId = css.getId()
                if ABSOLUTE_URL.match(cssPloneId):
                    css_jsList += "'%s', " % cssPloneId
                else:
                    cssPlone = '%s/portal_css/%s/%s' % (portal_url,
                                                        skinname,
                                                        cssPloneId)
                    css_jsList += "'%s', " % cssPlone

        baseres = '++resource++ckeditor_for_plone'
        css_jsList += "'%s/%s/ckeditor_plone_area.css']" % (portal_url,
                                                            baseres)

        return css_jsList

    def getCK_finder_url(self, type=None):
        """
        return browser url for a type
        """
        base_url = '%s/@@plone_ckfinder?' % self.ckfinder_basehref
        if type == 'file':
            base_url += 'typeview=file&media=file'
        elif type == 'flash':
            pid = 'browse_flashs_portal_types'
            flash_types = self.cke_properties.getProperty(pid)
            base_url += 'typeview=file&media=flash'
            for ftype in flash_types:
                base_url += '&types:list=%s' % url_quote(ftype)
        elif type == 'image':
            pid = 'browse_images_portal_types'
            image_types = self.cke_properties.getProperty(pid)
            base_url += 'typeview=image&media=image'
            for itype in image_types:
                base_url += '&types:list=%s' % url_quote(itype)
        return "'%s'" % base_url

    def geCK_JSProperty(self, prop):
        """
        just get property from ckeditor_properties sheet
        return it as a javascript string
        """
        cke_properties = self.cke_properties
        propValue = cke_properties.getProperty(prop)
        if type(propValue).__name__ in ('str', 'unicode'):
            return "'%s'" % propValue
        elif type(propValue).__name__ == 'bool':
            if propValue:
                return "true"
            else:
                return "false"
        elif type(propValue).__name__ == 'tuple':
            return str(list(propValue))
        elif propValue is not None:
            return str(cke_properties.getProperty(prop))

    def get_CK_image2_alignClasses(self):
        """check that each class is valid
        """
        cke_properties = self.cke_properties
        propValue = cke_properties.getProperty('image2_alignClasses')
        result = str(list(propValue))
        for class_ in propValue:
            # TODO: check that classes are valid according to HTML
            if not class_.strip():
                msg = ('At least a class among image2_alignClasses is not '
                       'valid: %s' % result)
                raise ValueError(msg)
        return result

    @property
    def cke_params(self):
        """
        return CKEditor widget Settings
        """
        params = {}
        cke_properties = self.cke_properties
        unchangedProps = ('width', 'height', 'bodyId', 'bodyClass', 'entities',
                          'entities_greek', 'entities_latin',
                          'forcePasteAsPlainText', 'toolbar',
                          'image2_captionedClass',
                          'defaultTableWidth')
        for p in unchangedProps:
            jsProp = self.geCK_JSProperty(p)
            if jsProp is not None:
                params[p] = jsProp

        params['image2_alignClasses'] = self.get_CK_image2_alignClasses()
        params['skin'] = "'{}'".format(
            cke_properties.getProperty('skin', 'moonocolor')
        )
        params['toolbar_Custom'] = cke_properties.getProperty('toolbar_Custom')
        params['contentsCss'] = self.getCK_contentsCss()
        params['filebrowserBrowseUrl'] = self.getCK_finder_url(type='file')
        img_url = self.getCK_finder_url(type='image')
        params['filebrowserImageBrowseUrl'] = img_url
        flash_url = self.getCK_finder_url(type='flash')
        params['filebrowserFlashBrowseUrl'] = flash_url
        # the basehref must be set in wysiwyg template
        # params['baseHref'] = self.cke_basehref
        params.update(self.cke_toolbars())
        return params

    def cke_toolbars(self):
        registry = getUtility(IRegistry)
        toolbars = registry['collective.ckeditor.toolbars']
        result = dict()
        for name, toolbar in toolbars.items():
            result['toolbar_{0}'.format(name)] = toolbar
        return result

    def getCK_plone_config(self):
        """
        return config for ckeditor
        as javascript file
        """
        request = self.request
        response = request.RESPONSE
        params_js_string = """CKEDITOR.editorConfig = function( config ) {"""
        params = self.cke_params
        for k, v in params.items():
            params_js_string += """
    config.%s = %s;
            """ % (k, v)

        ids = []
        for line in self.cke_properties.getProperty('plugins', []):
            # ignore the rest so we get no error
            if len(line.split(';')) == 2:
                id, url = line.split(';')
                abs_url = self.portal_url + url
                base_url, plugin = abs_url.rsplit('/', 1)
                ids.append(id)
                params_js_string += (
                    """CKEDITOR.plugins.addExternal('%s', '%s/', '%s');"""
                    % (id, base_url.rstrip('/'), plugin))
        params_js_string += '''config.extraPlugins = "%s";''' % ','.join(ids)

        removePlugins = self.cke_properties.getProperty('removePlugins', [])
        if removePlugins:
            params_js_string += (
                '''config.removePlugins = "%s";''' % ','.join(removePlugins))

        params_js_string += """
    config.filebrowserWindowWidth = parseInt(jQuery(window).width()*70/100);
    config.filebrowserWindowHeight = parseInt(jQuery(window).height()-20);
    config.toolbar_Basic = %s;
    config.toolbar_Plone = %s;
    config.toolbar_Full = %s;
    config.imageUploadUrl = '@@cke-upload-image';
    config.stylesSet = 'plone:%s/ckeditor_plone_menu_styles.js';
        """ % (CKEDITOR_BASIC_TOOLBAR,
               CKEDITOR_PLONE_DEFAULT_TOOLBAR,
               CKEDITOR_FULL_TOOLBAR,
               self.portal_url)
        cke_properties = self.cke_properties

        templatesReplaceContent = cke_properties.getProperty(
            'templatesReplaceContent')
        if templatesReplaceContent:
            params_js_string += """config.templates_replaceContent = true;"""
        else:
            params_js_string += """config.templates_replaceContent = false;"""

        use_disallowed_content = True
        filtering = cke_properties.getProperty('filtering')
        if filtering == 'default':
            extraAllowedContent = cke_properties.getProperty(
                'extraAllowedContent')
            params_js_string += "config.extraAllowedContent = {0};".format(
                extraAllowedContent)
        elif filtering == 'disabled':
            params_js_string += """config.allowedContent = true;"""
            # It is not possible to disallow content when the Advanced Content
            # Filter is disabled by setting CKEDITOR.config.allowedContent
            # to true.
            use_disallowed_content = False
        elif filtering == 'custom':
            customAllowedContent = cke_properties.getProperty(
                'customAllowedContent')
            params_js_string += "config.allowedContent = {0};".format(
                customAllowedContent)

        if use_disallowed_content:
            disallowedContent = cke_properties.getProperty(
                'disallowedContent')
            params_js_string += "config.disallowedContent = {0};".format(
                disallowedContent)

        # enable SCAYT on startup if necessary
        enableScaytOnStartup = cke_properties.getProperty(
            'enableScaytOnStartup')
        if enableScaytOnStartup:
            scayt_lang = self._getScaytLanguage()
            # if no relevant language could be found, do not activate SCAYT
            if scayt_lang:
                params_js_string += """config.scayt_autoStartup = true;"""
                params_js_string += """config.scayt_sLang = \
                    '%s';""" % scayt_lang
        else:
            params_js_string += """config.scayt_autoStartup = false;"""

        customTemplates = cke_properties.getProperty('customTemplates')
        if customTemplates:
            params_js_string += self.getCustomTemplatesConfig(customTemplates)
        params_js_string += """
};
        """

        cache_header = 'pre-check=0,post-check=0,must-revalidate,s-maxage=0,\
          max-age=0,no-cache'
        response.setHeader('Cache-control', cache_header)
        response.setHeader('Content-Type', 'application/x-javascript')

        return JavascriptPacker('safe').pack(params_js_string)

    def getCK_vars(self):
        return CK_VARS_TEMPLATE % {'portal_url': self.portal_url}

    def getCustomTemplatesConfig(self, customTemplates):
        templates = ["'%s/%s'," % (self.portal_url, template) for template in
                     customTemplates]
        result = """
    config.templates_files = [
        %s
        ];
""" % '\n'.join(templates)
        return result

    def getCK_plone_menu_styles(self):
        """
        return javascript for ckeditor
        plone menu styles
        """
        request = self.request
        response = request.RESPONSE
        cke_properties = self.cke_properties
        styles = demjson.loads(cke_properties.getProperty('menuStyles', '[]'))
        for style in styles:
            if 'name' in style:
                style['name'] = self.context.translate(_(style['name']))
        menu_styles_js_string = """
styles = jQuery.parseJSON('%s');
CKEDITOR.stylesSet.add('plone', styles);""" % demjson.dumps(styles)
        response.setHeader(
            'Cache-control',
            'pre-check=0,post-check=0,must-revalidate,'
            's-maxage=0,max-age=0,no-cache')
        response.setHeader('Content-Type', 'application/x-javascript')

        return JavascriptPacker('safe').pack(menu_styles_js_string)

    def customize_browserurl(self, settings, language):
        params = self.cke_params

        def update_setting(key):
            settings[key] = '%s&set_language=%s' % (params[key][1:-1], language)

        update_setting('filebrowserBrowseUrl')
        update_setting('filebrowserImageBrowseUrl')
        update_setting('filebrowserFlashBrowseUrl')

    def widget_settings(self, widget, fieldname):
        settings = IWidgetSettings(widget)
        settings.setup(ckview=self, fieldname=fieldname)
        return settings()


    def upload_image(self):
        container = component.getMultiAdapter((self.context, self.request),name='folder_factories').add_context()
        upload = self.request.form['upload']
        try:
            image = api.content.create(container=container, type='Image', file=upload, id=upload.filename, safe_id=True)
        except Unauthorized:
            LOG.warning("Upload image not allowed at {}".format(container.absolute_url()))
            raise
        navroot = api.portal.get_navigation_root(context=self.context)
        image_url = "/".join(('resolveuid', api.content.get_uuid(image)))
        result = {
            "uploaded": 1,
            "fileName": image.getId(),
            "url": image_url
        }
        return json.dumps(result)

    def _getScaytLanguage(self):
        """
        If SCAYT is enabled, try to select right default language.
        SCAYT language code is like 'fr_FR' or 'fr_CA', try to find out
        a corresponding language from the current content used language.
        If the current content language is not available in SCAYT languages,
        use the default site language.
        If it is not available neither, return None.
        """
        languageCodeToUse = None
        # get current content language or default site language
        default_language = self.context.portal_languages.getDefaultLanguage()
        content_language = self.context.Language() or default_language
        # content language can be like 'fr' or 'fr-be'...
        # be smart, compute language_code with
        # 2 first values and 2 last values...
        language_code = "%s_%s" % (content_language[0:2],
                                   content_language.upper()[-2:5])
        if language_code not in CKEDITOR_SUPPORTED_LANGUAGE_CODES:
            # try to find a fallback in available languages.
            # the fallback is the first language found with relevant
            # first part main language code.
            # So if we currently use 'fr-be' that has no corresponding
            # supported language in SCAYT, we will find the fallback for 'fr'
            # that is the first 'fr_xx' code found in SCAYT
            # supported languages...
            for supported_language in CKEDITOR_SUPPORTED_LANGUAGE_CODES:
                if supported_language.startswith(content_language[0:2]):
                    languageCodeToUse = supported_language
                    break
        else:
            languageCodeToUse = language_code
        return languageCodeToUse


class ckeditor_wysiwyg_support(BrowserView):
    index = ViewPageTemplateFile("templates/ckeditor_wysiwyg_support.pt")

    def __call__(self):
        return self.index()

    @property
    def macros(self):
        return self.index.macros


class IWidgetSettings(Interface):
    pass


class Z3WidgetSettings(object):
    implements(IWidgetSettings)

    def __init__(self, context):
        self.context = context

    def setup(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self):
        """
        Some params could be overloaded by widget settings
        """
        ckview = self.ckview
        widget = self.context
        widget_settings = {}
        if hasattr(widget, 'settings'):
            params = ckview.cke_params
            p_overloaded = ckview.cke_properties_overloaded
            for k, v in params.items():
                if k in p_overloaded and k in widget.settings:
                    widget_settings[k] = widget.settings[k]
            if 'language' in widget.settings:
                language = widget.settings['language']
                ckview.customize_browserurl(widget_settings, language)
        widget_settings['basehref'] = ckview.cke_basehref
        self.setupAjaxSave(widget_settings)
        return widget_settings

    def setupAjaxSave(self, widget_settings):
        portal = self.ckview.portal
        target = self.getSaveTarget()
        widget_settings['ajaxsave_enabled'] = 'true'
        try:
            save_url = str(portal.portal_url.getRelativeUrl(target) + '/cke-save')
            view = portal.restrictedTraverse(save_url)
        except:
            widget_settings['ajaxsave_enabled'] = 'false'
        else:
            widget_settings['ajaxsave_url'] = save_url
            widget_settings['ajaxsave_fieldname'] = self.getFieldName()


class Z3CFormWidgetSettings(Z3WidgetSettings):

    def getFieldName(self):
        widget = self.context
        field = widget.field
        return field.__name__

    def getSaveTarget(self):
        widget = self.context
        content_item = widget.context
        return content_item


class FormlibWidgetSettings(Z3WidgetSettings):

    def getFieldName(self):
        widget = self.context
        field = widget.context
        return field.__name__

    def getSaveTarget(self):
        widget = self.context
        field = widget.context
        content_item = field.context
        return content_item


class ATWidgetSettings(object):
    implements(IWidgetSettings)

    def __init__(self, context):
        self.context = context

    def setup(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self):
        """
        Some params could be overloaded by widget settings
        example : AT rich widget overload width or height
        """
        ckview = self.ckview
        params = ckview.cke_params
        widget = self.context
        widget_settings = {}
        p_overloaded = ckview.cke_properties_overloaded
        for k, v in params.items():
            if k in p_overloaded and hasattr(widget, k):
                widget_settings[k] = getattr(widget, k)
        # specific for cols and rows rich widget settings
        if hasattr(widget, 'cols') and 'width' not in p_overloaded:
            if widget.cols:
                width = str(int(int(widget.cols) * 100 / 40)) + '%'
                widget_settings['width'] = width
        if hasattr(widget, 'rows') and 'height' not in p_overloaded:
            if widget.rows:
                height = str(int(widget.rows) * 25) + 'px'
                widget_settings['height'] = height
        if hasattr(widget, 'language'):
            ckview.customize_browserurl(widget_settings, widget.language)
        widget_settings['basehref'] = ckview.cke_basehref
        widget_settings['language'] = ckview.cke_language
        self.setupAjaxSave(widget_settings)
        return widget_settings

    def setupAjaxSave(self, widget_settings):
        widget_settings['ajaxsave_enabled'] = 'true'
        widget_settings['ajaxsave_fieldname'] = self.fieldname
        widget_settings['ajaxsave_url'] = self.ckview.context.absolute_url() + '/cke-save'

class AjaxSave(BrowserView):

    def AT_save(self, fieldname, text):
        self.context.getField(fieldname).set(self.context,
                                             text,
                                             mimetype='text/html')
        return "saved"

    def portlet_save(self, fieldname, text):
        setattr(self.context, fieldname, text.decode('utf8'))
        return "saved"

    def dexterity_save(self, fieldname, text):
        from plone.app.textfield.value import RichTextValue
        value = RichTextValue(text)
        setattr(self.context, fieldname, value)
        return "saved"
