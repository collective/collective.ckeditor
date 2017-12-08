# -*- coding: utf-8 -*-
import unittest
import json
from plone import api

from zope.component import getMultiAdapter
from ..testing import CKEDITOR_INTEGRATION
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class TestCKeditorViewTestCase(unittest.TestCase):
    """Test the methods of the CKeditorView."""

    layer = CKEDITOR_INTEGRATION

    def test_getScaytLanguage(self):
        """
          Test the ckeditor_view._getScaytLanguage method.
          This method will try to find out the SCAYT language to use in case
          SCAYT is enabled on CKeditor widget startup.
          It tries to map the current content used language with languages
          codes supported by SCAYT.
        """
        portal = self.layer['portal']
        from Products.CMFPlone import utils as ploneutils
        ploneutils._createObjectByType('Document', portal, 'front-page')
        frontPage = getattr(portal, 'front-page')
        view = getMultiAdapter(
            (frontPage, frontPage.REQUEST),
            name='ckeditor_view'
        )
        # by default, frontPage language is 'en'
        self.assertEquals(frontPage.Language(), 'en')
        self.assertEquals(view._getScaytLanguage(), 'en_US')
        # define another language for frontPage
        frontPage.setLanguage('fr')
        # used language will now be fr_FR
        self.assertEquals(view._getScaytLanguage(), 'fr_FR')
        # define a language with sub language
        frontPage.setLanguage('fr-ca')
        # as fr-ca is supported, it will be used
        self.assertEquals(view._getScaytLanguage(), 'fr_CA')
        # if NOT supported, the language can not be determined, it returns None
        frontPage.setLanguage('ru')
        self.failIf(view._getScaytLanguage())
        frontPage.setLanguage('ru-ru')
        self.failIf(view._getScaytLanguage())

    def test_uploadimage(self):

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        view = getMultiAdapter(
            (portal, portal.REQUEST),
            name='cke-upload-image'
        )
        view.request.form['upload'] = DummyFileUpload(filename="image1.png")
        view()
        self.failIf("image1.png" not in portal.objectIds())
        self.assertEquals(portal['image1.png'].portal_type, 'Image')
        view()
        self.failIf("image1-1.png" not in portal.objectIds())
        self.assertEquals(portal['image1-1.png'].portal_type, 'Image')
    
    def test_uploadimage_json(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        view = getMultiAdapter(
            (portal, portal.REQUEST),
            name='cke-upload-image'
        )
        view.request.form['upload'] = DummyFileUpload(filename="image1.png")
        result = json.loads(view())
        self.assertTrue('url' in result)
        self.assertTrue('fileName' in result)
        self.assertEquals(result['fileName'], 'image1.png')
        self.assertTrue('uploaded' in result)
        self.assertEquals(result['uploaded'], 1)

    def test_uploadimage_url(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        view = getMultiAdapter(
            (portal, portal.REQUEST),
            name='cke-upload-image'
        )
        view.request.form['upload'] = DummyFileUpload(filename="image1.png")
        result = json.loads(view())
        self.assertTrue('url' in result)
        msg = "url should contain resolveuid"
        self.assertTrue('resolveuid' in result['url'], msg)
        uuid = result['url'].split('/')[-1]
        image = portal['image1.png']
        self.assertEquals(api.content.get_uuid(image), uuid)

from plone.app.blob.interfaces import IFileUpload
from zope.interface import implements

class DummyFileUpload:
    
    implements(IFileUpload)

    def __init__(self, data='', filename='', content_type=''):
        self.data = data
        self.filename = filename
        self.headers = {'content_type': content_type}

    def read(self, index=None):
        if index is None:
            index = len(self.data)
        return self.data[:index]

    def tell(self):
        return len(self.data)

    def seek(self, offset, from_what=0):
        pass
