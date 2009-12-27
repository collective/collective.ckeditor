from Acquisition import aq_inner
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
        context = aq_inner(context)                                              
        session = request.get('SESSION', None)    
        # store CKEditor function name in session for ajax calls
        session.set('CKEditorFuncNum', request.get('CKEditorFuncNum', ''))    
        self.jsaddons = self.get_jsaddons()


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