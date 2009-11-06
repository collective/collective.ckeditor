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