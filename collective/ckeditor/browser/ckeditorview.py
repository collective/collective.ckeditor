from Acquisition import aq_inner
from zope import component
from zope.interface import implements, Interface
from zope.app.component.hooks import getSite
from Products.PythonScripts.standard import url_quote
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.tools.packer import JavascriptPacker
from collective.ckeditor.config import CKEDITOR_PLONE_DEFAULT_TOOLBAR

CK_VARS_TEMPLATE = """
// set the good base path for the editor because
// portal_javascripts loose it
// otherwise ckeditor linked urls are bad
// important : this script must be called before ckeditor.js

var CKEDITOR_BASEPATH = '%(portal_url)s/++resource++ckeditor/';
var CKEDITOR_PLONE_BASEPATH = '%(portal_url)s/++resource++ckeditor_for_plone/';
var CKEDITOR_PLONE_PORTALPATH = '%(portal_url)s';
"""


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
        self.portal = getSite()
        self.portal_url = self.portal.absolute_url()
        request.set('ckLoaded', True)

    @property
    def cke_properties(self):
        pp = getToolByName(self.portal, 'portal_properties')
        return pp.ckeditor_properties

    @property
    def cke_config_url(self):
        """"
        return the dynamic configuration file url
        """
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
        return member.getProperty('wysiwyg_editor') == 'CKeditor'

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
                fieldname, context.getContentType(fieldname))
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

    @property
    def cke_params(self):
        """
        return CKEditor widget Settings
        """
        params = {}
        cke_properties = self.cke_properties
        unchangedProps = ('width', 'height', 'bodyId', 'bodyClass', 'entities',
                          'entities_greek', 'entities_latin',
                          'forcePasteAsPlainText', 'toolbar')
        for p in unchangedProps:
            jsProp = self.geCK_JSProperty(p)
            if jsProp is not None:
                params[p] = jsProp

        params['toolbar_Custom'] = cke_properties.getProperty('toolbar_Custom')
        params['contentsCss'] = self.getCK_contentsCss()
        params['filebrowserBrowseUrl'] = self.getCK_finder_url(type='file')
        img_url = self.getCK_finder_url(type='image')
        params['filebrowserImageBrowseUrl'] = img_url
        flash_url = self.getCK_finder_url(type='flash')
        params['filebrowserFlashBrowseUrl'] = flash_url
        # the basehref must be set in wysiwyg template
        # params['baseHref'] = self.cke_basehref

        return params

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

        ids=[]
        for line in self.cke_properties.getProperty('plugins',''):
            #ignore the rest so we get no error
            if len(line.split(';'))==2:
                id,url=line.split(';')
                abs_url=self.portal_url+url
                ids.append(id)
                params_js_string+="""CKEDITOR.plugins.addExternal( '%s', '%s' );"""%(id,abs_url)
        params_js_string+= '''config.extraPlugins = "%s";'''%','.join(ids)

        params_js_string += """
    config.filebrowserWindowWidth = parseInt(jQuery(window).width()*70/100);
    config.filebrowserWindowHeight = parseInt(jQuery(window).height()-20);
    config.toolbar_Plone = %s;
    config.stylesSet = 'plone:%s/ckeditor_plone_menu_styles.js';
        """ % (CKEDITOR_PLONE_DEFAULT_TOOLBAR, self.portal_url)
        cke_properties = self.cke_properties
        templatesReplaceContent = cke_properties.getProperty('templatesReplaceContent')
        if templatesReplaceContent:
            params_js_string += """config.templates_replaceContent = true;"""
        else:
            params_js_string += """config.templates_replaceContent = false;"""
        customTemplates = cke_properties.getProperty('customTemplates')
        if customTemplates:
            params_js_string += self.getCustomTemplatesConfig(customTemplates)
        params_js_string += """
};
        """

        pstate = component.getMultiAdapter((self.context, self.request),
                                           name="plone_portal_state")
        language = pstate.language()
        params_js_string += "CKEDITOR.config.language = '%s';" % language

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
        menu_styles_js_string = """
CKEDITOR.stylesSet.add('plone',
%s );""" % str(cke_properties.getProperty('menuStyles', []))
        response.setHeader('Cache-control',
                           'pre-check=0,post-check=0,must-revalidate,s-maxage=0,max-age=0,no-cache')
        response.setHeader('Content-Type', 'application/x-javascript')

        return JavascriptPacker('safe').pack(menu_styles_js_string)

    def getCK_widget_settings(self, widget):
        """
        Some params could be overloaded
        for a local field
        by widget settings
        example : AT rich widget overload width or height
        TODO : specific AT widget or Dexterity Widget with all ckeditor params
        """
        params = self.cke_params
        cke_properties = self.cke_properties
        p_overloaded = cke_properties.getProperty('properties_overloaded', [])
        if widget is not None:
            widget_settings = {}
            for k, v in  params.items():
                if hasattr(widget, k) and not k in p_overloaded:
                    widget_settings[k] = v

            # specific for cols and rows rich widget settings
            if hasattr(widget, 'cols') and not 'width' in p_overloaded:
                if widget.cols:
                    width = str(int(int(widget.cols) * 100 / 40)) + '%'
                    widget_settings['width'] = width
            if hasattr(widget, 'rows') and not 'height' in p_overloaded:
                if widget.rows:
                    height = str(int(widget.rows) * 25) + 'px'
                    widget_settings['height'] = height

            return widget_settings

    def ajaxsave(self, fieldname, text):
        self.context.getField(fieldname).set(self.context,
                                             text,
                                             mimetype='text/html')
        return "saved"


class ckeditor_wysiwyg_support(BrowserView):
    index = ViewPageTemplateFile("templates/ckeditor_wysiwyg_support.pt")

    def __call__(self):
        return self.index()

    @property
    def macros(self):
        return self.index.macros
