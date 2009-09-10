from Acquisition import aq_inner
from zope.interface import implements, Interface
from zope.app.component.hooks import getSite

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.ckeditor import siteMessageFactory as _

class ICKeditorView(Interface):
    """
    CKeditor browser view interface
    """
    def contentUsesCKeditor():
        """return True or False when CKeditor can be used or not"""    


    
class CKeditorView(BrowserView):
    """
    CKeditor browser view
    """
    implements(ICKeditorView)

    def __init__(self, context, request):
        self.context = context
        self.request = request    
        self.portal = getSite()
        request.set('ckLoaded',True)
        
    def _memberUsesCKeditor(self):
        """return True if member uses CKeditor"""
        pm = getToolByName(self.portal, 'portal_membership')
        return pm.getAuthenticatedMember().getProperty('wysiwyg_editor')=='CKeditor'
    
    def contentUsesCKeditor(self, fieldname=''):
        """
        data for view
        """        
        context= aq_inner(self.context)   
        request = self.request 
        if self. _memberUsesCKeditor() :
            if not fieldname :
                return True
            if not hasattr(context, 'getField'):
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

    def getCK_params(self) :
        """
        return CK Control Panel Settings or widget Settings
        """            
        
        