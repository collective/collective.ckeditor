# -*- coding: utf-8 -*-

"""Base class for ckeditor test cases.
"""

from zope.component import getMultiAdapter
from collective.ckeditor.tests.base import CKEditorTestCase


class TestCKeditorViewTestCase(CKEditorTestCase):
    """Test the methods of the CKeditorView."""

    def test_determinateScaytLanguageToUse(self):
        """
          This method will try to find out the SCAYT language to use in case
          SCAYT is enabled on CKeditor widget startup.
          It tries to map the current member used language with languages codes
          supported by SCAYT.
        """
        req = self.portal.REQUEST
        view = getMultiAdapter((self.portal, req), name='ckeditor_view')
        # by default, nothing in the REQUEST.HTTP_ACCEPT_LANGUAGE,
        # the default portal language is used
        defaultPortalLanguage = self.portal.portal_languages.getDefaultLanguage()
        self.assertEquals(defaultPortalLanguage, 'en')
        self.assertEquals(req.get('HTTP_ACCEPT_LANGUAGE'), '')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'en_US')
        # define another portal default_language
        self.portal.portal_languages.setDefaultLanguage('fr')
        # used language will now be fr_FR
        self.assertEquals(req.get('HTTP_ACCEPT_LANGUAGE'), '')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_FR')
        # now play with HTTP_ACCEPT_LANGUAGE
        req.set('HTTP_ACCEPT_LANGUAGE', 'pt')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'pt_PT')
        req.set('HTTP_ACCEPT_LANGUAGE', 'fr-be,en;q=0.5')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_FR')
        req.set('HTTP_ACCEPT_LANGUAGE', 'fr-ca,en;q=0.5')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_CA')
        req.set('HTTP_ACCEPT_LANGUAGE', 'ru,uk;q=0.5')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'en_US')
