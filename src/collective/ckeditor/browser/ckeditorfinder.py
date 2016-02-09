from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from collective.plonefinder.browser.finder import Finder


class CKFinder(Finder):
    """
    Custom Finder class for CKEditor
    """

    def __init__(self, context, request):
        super(CKFinder, self).__init__(context, request)
        self.findername = 'plone_ckfinder'
        self.multiselect = False
        self.allowupload = True
        self.allowaddfolder = True
        context = aq_inner(context)

    def __call__(self):

        context = aq_inner(self.context)
        request = aq_inner(self.request)
        session = request.get('SESSION', {})

        pp = getToolByName(context, 'portal_properties')
        ckprops = pp.ckeditor_properties
        self.allowaddfolder = ckprops.getProperty('allow_folder_creation',
                                                  self.allowaddfolder)

        self.showbreadcrumbs = request.get(
            'showbreadcrumbs',
            self.showbreadcrumbs
        )
        # scopeInfos must be set here because we need it in  set_session_props
        self.setScopeInfos(context, request, self.showbreadcrumbs)
        # store CKEditor function name in session for ajax calls
        if session:
            session.set('CKEditorFuncNum', request.get('CKEditorFuncNum', ''))
        # redefine some js methods (to select items ...)
        self.jsaddons = self.get_jsaddons()
        # set media type
        self.set_media_type()
        # store some properties in session
        # (portal_type used for upload and folder creation ...)
        self.set_session_props()
        # the next call to setScopeInfos must be empty
        self.setScopeInfos = self.empty_setScopeInfos
        return super(CKFinder, self).__call__()

    def empty_setScopeInfos(self, context, request, showbreadcrumbs):
        """
        setScopeInfos redefined (the job is done before Finder.__call__() )
        """
        pass

    def set_media_type(self):
        """
        set media type used for ckeditor
        """
        request = self.request
        self.media = request.get('media', 'file')

    def set_session_props(self):
        """
        Take some properties from ckeditor to store in session
        """
        request = self.request
        session = request.get('SESSION', {})

        session.set('media', self.media)

        # typeupload (portal_type used for upload)
        self.typeupload = self.get_type_for_upload(self.media)
        if session:
            session.set('typeupload', self.typeupload)

        # mediaupload
        # the mediaupload force the content-type selection in fileupload
        # see quick_upload.py in collective.quickupload
        # example (*.jpg, *.gif, ...) when media='image'
        if session:
            if self.media != 'file':
                session.set('mediaupload', self.media)
            else:
                session.set('mediaupload', '*.*')

        # typefolder
        self.typefolder = self.get_type_for_upload('folder')
        if session:
            session.set('typefolder', self.typefolder)

    def get_type_for_upload(self, media):
        """
        return CKeditor settings for unik media_portal_type
        """
        context = aq_inner(self.context)

        pprops = getToolByName(context, 'portal_properties')
        ckprops = pprops.ckeditor_properties

        prop = ckprops.getProperty('%s_portal_type' % media)

        if prop == 'auto':
            return ''
        elif prop != 'custom':
            return prop

        scopetype = self.scopetype

        # custom type depending on scope
        mediatype = ''
        customprop = ckprops.getProperty('%s_portal_type_custom' % media)
        for pair in customprop:
            listtypes = pair.split('|')
            if listtypes[0] == '*':
                mediatype = listtypes[1]
            elif listtypes[0] == scopetype:
                mediatype = listtypes[1]
                break
        return mediatype

    def get_jsaddons(self):
        """
        redefine selectItem method
        in js string
        """
        request = aq_inner(self.request)
        session = request.get('SESSION', {})
        CKEditorFuncNum = session.get('CKEditorFuncNum', '')

        jsstring = """
selectCKEditorItem = function (selector, title, image_preview) {
 image_preview = (typeof image_preview != "undefined") ? image_preview : false;
 if (image_preview) selector = selector + '/@@images/image/preview' ;
 window.opener.CKEDITOR.tools.callFunction( %s, 'resolveuid/' + selector );
 window.close();
};
Browser.selectItem = selectCKEditorItem;
             """ % CKEditorFuncNum

        return jsstring
