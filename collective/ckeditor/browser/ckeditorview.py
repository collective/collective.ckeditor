from Acquisition import aq_inner
from zope.interface import implements, Interface
from zope.app.component.hooks import getSite
from Products.PythonScripts.standard import url_quote
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.tools.packer import JavascriptPacker
from collective.ckeditor import siteMessageFactory as _
from collective.ckeditor.config import CKEDITOR_PLONE_DEFAULT_TOOLBAR
from collective.ckeditor import LOG

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
        request.set('ckLoaded',True)
        
    @property
    def cke_properties(self) :
        pp = getToolByName(self.portal, 'portal_properties')
        return pp.ckeditor_properties
        
    @property
    def cke_config_url(self) :
        """"
        return the dynamic configuration file url
        """
        context = aq_inner(self.context)
        return '%s/ckeditor_plone_config.js' %context.absolute_url()

    @property
    def cke_basehref(self) :
        """
        return the base href used by ckeditor
        to calculate relative or absolute links
        during edition (when copy pasting urls)
        by default it's the actual url
        """           
        request = self.request
        return "%s" %request['ACTUAL_URL']

    @property
    def cke_result_basehref(self) :
        """
        return the base href
        used to calculate relative or absolute links
        after edition
        by default it's the global renderBase value
        """           
        context= aq_inner(self.context) 
        plone_view = context.restrictedTraverse('@@plone')
        return "'%s'" %plone_view.renderBase()

    @ property
    def ckfinder_basehref(self) :
        """
        return CK finder base href
        TODO : improve it with control panel
        (could be a specific place in site)
        """           
        context= aq_inner(self.context) 
        return context.absolute_url()

    def _memberUsesCKeditor(self):
        """return True if member uses CKeditor"""
        pm = getToolByName(self.portal, 'portal_membership')
        return pm.getAuthenticatedMember().getProperty('wysiwyg_editor')=='CKeditor'
    
    def contentUsesCKeditor(self, fieldname=''):
        """
        return True if content uses CKeditor
        """        
        context= aq_inner(self.context)   
        request = self.request 
        if self. _memberUsesCKeditor() :
            if not fieldname :
                return True
            if not hasattr(context, 'getField'):
                return True    
            field = context.getField(fieldname)
            if not field:
                return True
            text_format = request.get('%s_text_format' % fieldname, context.getContentType(fieldname))
            content = field.getEditAccessor(context)()
            try:
                if content.startswith('<!--'):
                    return False
            except :
                return False
            return len(content)==0 or 'html' in text_format.lower()                
        return False

    def getCK_contentsCss(self) :
        """
        return list of style sheets applied to ckeditor area
        the list is returned as a javascript string
        by default portal_css mixin + plone_ckeditor_area.css
        TODO : improve it with a control panel
        """
        context= aq_inner(self.context) 
        portal = self.portal
        portal_url = self.portal_url
        portal_css = getToolByName(portal, 'portal_css')
        css_jsList="["        
        current_skin= context.getCurrentSkinName()
        skinname = url_quote(current_skin)
        css_res= portal_css.getEvaluatedResources(context)
        for css in css_res :
           if css.getMedia() not in ('print', 'projection') and css.getRel()=='stylesheet' :
             cssPloneId = css.getId()
             cssPlone= '%s/portal_css/%s/%s' %(portal_url, skinname, cssPloneId)
             css_jsList += "'%s', " %cssPlone  
        
        
        css_jsList += "'%s/++resource++ckeditor_for_plone/ckeditor_plone_area.css']" %portal_url  
        
        return css_jsList      
        
        
    def getCK_finder_url(self, type) :
        """
        return browser url for a type
        """
        base_url = '%s/@@plone_ckfinder?' % self.ckfinder_basehref
        if type == 'file' :
            base_url += 'typeview=file&media=file'
        elif type == 'flash' :
            flash_types = self.cke_properties.getProperty('browse_flashs_portal_types')
            base_url += 'typeview=file&media=flash'
            for type in flash_types :
                base_url += '&types:list=%s' %url_quote(type)
        elif type == 'image' :
            image_types = self.cke_properties.getProperty('browse_images_portal_types')
            base_url += 'typeview=image&media=image'
            for type in image_types :
                base_url += '&types:list=%s' %url_quote(type)
        return "'%s'" %base_url

    def geCK_JSProperty(self, property) :
        """
        just get property from ckeditor_properties sheet
        return it as a javascript string
        """        
        cke_properties = self.cke_properties
        propValue = cke_properties.getProperty(property)
        if type(propValue).__name__ in ('str', 'unicode'):
            return "'%s'" %propValue
        elif type(propValue).__name__ == 'bool' :
            if propValue :
                return "true"
            else :
                return "false"
        elif type(propValue).__name__ == 'tuple' :
            return str(list(propValue))
        elif propValue is not None :
            return str(cke_properties.getProperty(property))
    
    @property
    def cke_params(self) :
        """
        return CKEditor widget Settings
        """         
        params = {}
        cke_properties = self.cke_properties
        unchangedProps = ('width', 'height', 'bodyId', 'bodyClass', 'entities',
                          'entities_greek', 'entities_latin', 'forcePasteAsPlainText',
                          'toolbar')
        for p in unchangedProps :
            jsProp = self.geCK_JSProperty(p)
            if jsProp is not None :
                params[p] = jsProp

        params['toolbar_Custom'] = cke_properties.getProperty('toolbar_Custom')
        params['contentsCss'] = self.getCK_contentsCss()
        params['filebrowserBrowseUrl'] = self.getCK_finder_url(type='file')
        params['filebrowserImageBrowseUrl'] = self.getCK_finder_url(type='image')
        params['filebrowserFlashBrowseUrl'] = self.getCK_finder_url(type='flash')
        # the basehref must be set in wysiwyg template
        # params['baseHref'] = self.cke_basehref
        
        return params

    def getCK_plone_config(self) :
        """
        return config for ckeditor
        as javascript file
        """
        request = self.request
        response = request.RESPONSE
        params_js_string = """
CKEDITOR.editorConfig = function( config )
{
        """
        params = self.cke_params
        for k, v in params.items() :
            params_js_string += """
    config.%s = %s;
            """ %(k, v)
        
        params_js_string +="""
    config.filebrowserWindowWidth = parseInt(jQuery(window).width()*70/100);
    config.filebrowserWindowHeight = parseInt(jQuery(window).height()-20);
    config.toolbar_Plone = %s;
    config.stylesSet = 'plone:%s/ckeditor_plone_menu_styles.js';
};
        """ % (CKEDITOR_PLONE_DEFAULT_TOOLBAR, self.portal_url)
        response.setHeader('Cache-control','pre-check=0,post-check=0,must-revalidate,s-maxage=0,max-age=0,no-cache')
        response.setHeader('Content-Type', 'application/x-javascript')
        
        return JavascriptPacker('safe').pack(params_js_string)

    def getCK_plone_menu_styles(self) :
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
        response.setHeader('Cache-control','pre-check=0,post-check=0,must-revalidate,s-maxage=0,max-age=0,no-cache')
        response.setHeader('Content-Type', 'application/x-javascript')
        
        return JavascriptPacker('safe').pack(menu_styles_js_string)

    def getCK_widget_settings(self, widget) :
        """
        Some params could be overloaded
        for a local field
        by widget settings
        example : AT rich widget overload width or height
        TODO : specific AT widget or Dexterity Widget with all ckeditor params
        """
        params = self.cke_params
        cke_properties = self.cke_properties
        properties_overloaded = cke_properties.getProperty('properties_overloaded', [])
        if widget is not None :
            widget_settings = {}
            for k, v in  params.items() :
                if hasattr(widget, k) and not k in properties_overloaded :
                    widget_settings[k] = v

            # specific for cols and rows rich widget settings
            if hasattr(widget, 'cols') and not 'width' in properties_overloaded :
                if widget.cols :
                    widget_settings['width'] = str(int(int(widget.cols)*100/40)) + '%'
            if hasattr(widget, 'rows') and not 'height' in properties_overloaded :
                if widget.rows :
                    widget_settings['height'] = str(int(widget.rows)*25) + 'px'
            
            return widget_settings
                    
        