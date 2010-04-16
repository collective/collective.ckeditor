from Acquisition import aq_base, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.plonefinder.browser.finder import Finder



class CKFinder(Finder):
    """
    Custom Finder class for CKEditor
    """
    
    def __init__(self, context, request) :
        super(CKFinder, self).__init__(context, request)    
        self.findername = 'plone_ckfinder'
        self.multiselect = False 
        self.allowupload = True
        self.allowaddfolder = True
        context = aq_inner(context) 
    
    def __call__(self):
    
        context = aq_inner(self.context)
        request = aq_inner(self.request)                                       
        session = request.get('SESSION', None)  
        self.showbreadcrumbs =  request.get('showbreadcrumbs', self.showbreadcrumbs)
        # scopeInfos must be set here because we need it in  set_session_props
        self._newSetScopeInfos(context, request, self.showbreadcrumbs)     
        # store CKEditor function name in session for ajax calls
        session.set('CKEditorFuncNum', request.get('CKEditorFuncNum', ''))    
        # redefine some js methods (to select items ...)
        self.jsaddons = self.get_jsaddons()
        # set media type
        self.set_media_type()
        # store some properties in session (portal_type used for upload and folder creation ...)
        self.set_session_props()
        return super(CKFinder, self).__call__()
        
    def _newSetScopeInfos(self, context, request, showbreadcrumbs):
        """
        set scope and all infos related to scope
        setScopeInfos redefined to be called before super(CKFinder, self).__call__()
        """
        browsedpath = request.get('browsedpath', self.browsedpath)
        # find scope if undefined
        # by default scope = browsedpath or first parent folderish or context if context is a folder        
        scope = self.scope
        if scope is None  : 
            if browsedpath :
                self.scope = scope = aq_inner(self.portal.restrictedTraverse(browsedpath))   
            else :
                folder = aq_inner(context)
                while not IPloneSiteRoot.providedBy(folder)  : 
                    if bool(getattr(aq_base(folder), 'isPrincipiaFolderish', False)) :
                        break
                    folder = aq_inner(folder.aq_parent)    
                self.scope = scope = folder 
                
        self.scopetitle = scope.Title()          
        self.scopetype = scopetype = scope.portal_type 
        self.scopeiconclass = 'contenttype-%s divicon' % scopetype.lower().replace(' ','-')
        
        # set browsedpath and browsed_url
        if not IPloneSiteRoot.providedBy(scope) : 
            self.browsedpath = '/'.join(scope.getPhysicalPath())        
            self.browsed_url = scope.absolute_url()
            parentscope = aq_inner(scope.aq_parent)
            if not IPloneSiteRoot.providedBy(parentscope) :
                self.parentpath = '/'.join(parentscope.getPhysicalPath()) 
            else :
                self.parentpath =  self.portalpath   
        else :
            self.browsedpath = self.portalpath
            self.browsed_url = self.portal_url     
        
        # set breadcrumbs    
        # TODO : use self.catalog                     
        if showbreadcrumbs :
            crumbs = []
            item = scope
            while not IPloneSiteRoot.providedBy(item) :
                 crumb = {}
                 crumb['path'] = '/'.join(item.getPhysicalPath())
                 crumb['title'] = item.title_or_id()
                 crumbs.append(crumb)
                 item = aq_inner(item.aq_parent)
            crumbs.reverse()
            self.breadcrumbs = crumbs         
    
    def setScopeInfos(self, context, request, showbreadcrumbs):
        """
        setScopeInfos redefined (the job is done before Finder.__call__() by __newSetScopeInfos )
        """
        pass

    def set_media_type(self) :
        """
        set media type used for ckeditor
        """
        request = self.request                                       
        session = request.get('SESSION', None)
        self.media = session.get('media', request.get('media', 'file'))
    
    def set_session_props(self):
        """
        Take some properties from ckeditor to store in session
        """   
        request = self.request                                       
        session = request.get('SESSION', None)
        
        session.set('media', self.media)
        
        # typeupload
        self.typeupload = self.get_type_for_media(self.media)
        session.set('typeupload', self.typeupload)
        
        # typefolder
        self.typefolder = self.get_type_for_media('folder')
        session.set('typefolder', self.typefolder)        
            
        
    def get_type_for_media(self, media) :
        """
        return CKeditor settings for unik media_portal_type
        """
        context = aq_inner(self.context)
        request = self.request                                       
        session = request.get('SESSION', None)
        
        pprops = getToolByName(context, 'portal_properties')
        ckprops = pprops.ckeditor_properties
        
        prop = ckprops.getProperty('%s_portal_type' %media)
        
        if prop == 'auto' :
            return ''
        elif prop != 'custom' :
            return prop
        
        scopetype = self.scopetype
        
        # custom type depending on scope
        mediatype = ''
        customprop = ckprops.getProperty('%s_portal_type_custom' %media)        
        for pair in customprop :
            listtypes = pair.split('|')
            if listtypes[0]=='*' :
                mediatype = listtypes[1]
            elif listtypes[0]== scopetype :    
                mediatype = listtypes[1]
                break        
        return mediatype        
        

    def get_jsaddons(self) :
        """
        redefine selectItem method
        in js string
        """    
        context = aq_inner(self.context)
        request = aq_inner(self.request)                                       
        session = request.get('SESSION', None)
        CKEditor = session.get('CKEditor', '')
        CKEditorFuncNum = session.get('CKEditorFuncNum', '')
        
        jsstring = """
selectCKEditorItem = function (UID) {
	window.opener.CKEDITOR.tools.callFunction( %s, './resolveuid/' + UID );
	window.close();
};
Browser.selectItem = selectCKEditorItem;
             """ % CKEditorFuncNum
        
        return jsstring