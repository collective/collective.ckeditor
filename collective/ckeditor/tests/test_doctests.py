# -*- coding: utf-8 -*-  

from zope.testing import doctest
from unittest import TestSuite, main
from Testing import ZopeTestCase as ztc
from collective.ckeditor.tests.base import CKEditorTestCase



OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    tests = [ 'installation.txt',
              'controlpanel.txt',
              'ckeditor_jsconfig.txt',
              'uninstall.txt',
              'widget.txt',
              'transform_uids.txt',
             ]
    suite = TestSuite()
    for test in tests:
        suite.addTest(ztc.FunctionalDocFileSuite(test,
            optionflags=OPTIONFLAGS,
            package="collective.ckeditor.tests",
            test_class=CKEditorTestCase))
    return suite

