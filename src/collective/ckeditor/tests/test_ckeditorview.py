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
        frontPage = getattr(self.portal, 'front-page')
        view = getMultiAdapter((frontPage, frontPage.REQUEST), name='ckeditor_view')
        # by default, frontPage language is 'en'
        self.assertEquals(frontPage.Language(), 'en')
        self.assertEquals(view._determinateScaytLanguageToUse(), 'en_US')
        # define another language for frontPage
        frontPage.setLanguage('fr')
        # used language will now be fr_FR
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_FR')
        # define a language with sub language
        frontPage.setLanguage('fr-ca')
        # as fr-ca is supported, it will be used
        self.assertEquals(view._determinateScaytLanguageToUse(), 'fr_CA')
        # if NOT supported, the language can not be determined, it returns None
        frontPage.setLanguage('ru')
        self.failIf(view._determinateScaytLanguageToUse())
        frontPage.setLanguage('ru-ru')
        self.failIf(view._determinateScaytLanguageToUse())
