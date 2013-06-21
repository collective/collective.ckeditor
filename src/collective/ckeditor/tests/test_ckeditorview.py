# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from collective.ckeditor.tests.base import CKEditorTestCase


class TestCKeditorViewTestCase(CKEditorTestCase):
    """Test the methods of the CKeditorView."""

    def test_determinateScaytLanguageToUse(self):
        """
          Test the ckeditor_view._determinateScaytLanguageToUse method.
          This method will try to find out the SCAYT language to use in case
          SCAYT is enabled on CKeditor widget startup.
          It tries to map the current content used language with languages codes
          supported by SCAYT.
        """
        view = getMultiAdapter((self.portal, self.portal.REQUEST), name='ckeditor_view')
        # by default, self.portal language is 'en'
        self.assertEquals(self.portal.Language(), 'en')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'en_US')
        # define another language for portal
        self.portal.setLanguage('fr')
        # used language will now be fr_FR
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_FR')
        # define a language with sub language
        self.portal.setLanguage('fr-ca')
        # if supported, the relevant language is used
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_CA')
        # if NOT supported, the relevant fallback language is used
        self.portal.setLanguage('ru')
        self.failIf(view._determinateScaytLanguageToUse())
        self.portal.setLanguage('ru-ru')
        self.failIf(view._determinateScaytLanguageToUse())
