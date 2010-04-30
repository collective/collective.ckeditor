# -*- coding: utf-8 -*-

"""Base class for ckeditor test cases.
"""

import sys
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five.testbrowser import Browser
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """
    Set up the package and its dependencies.
    """    
    
    fiveconfigure.debug_mode = True
    import collective.ckeditor
    zcml.load_config('configure.zcml',collective.ckeditor)
    #fiveconfigure.debug_mode = False    
    ztc.installPackage('collective.ckeditor')    

setup_product()
ptc.setupPloneSite(products=['collective.ckeditor'])


class CKEditorTestCase(ptc.FunctionalTestCase):
    """base test case with convenience methods for all ckeditor tests""" 
    
    def afterSetUp(self):
        super(CKEditorTestCase, self).afterSetUp()        
        self.browser = Browser()        
        self.uf = self.portal.acl_users
        self.uf.userFolderAddUser('root', 'secret', ['Manager'], [])        
        self.ptool = getToolByName(self.portal, 'portal_properties')    
    
    def loginAsManager(self, user='root', pwd='secret'):
        """points the browser to the login screen and logs in as user root with Manager role."""
        self.browser.open('http://nohost/plone/')
        self.browser.getLink('Log in').click()
        self.browser.getControl('Login Name').value = user
        self.browser.getControl('Password').value = pwd
        self.browser.getControl('Log in').click()
    
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            # doctests don't play nicely with ipython
            try :
                iphook = sys.displayhook
                sys.displayhook = sys.__displayhook__
            except:
                pass    

        @classmethod
        def tearDown(cls):
            try :
                 sys.displayhook = iphook
            except:
                pass    

