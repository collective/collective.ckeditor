# -*- coding: utf-8 -*-
import unittest
import doctest

from plone.testing import layered

from ..testing import CKEDITOR_FUNCTIONAL


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

doc_tests = [
    'installation.txt',
    'controlpanel.txt',
    'ckeditor_jsconfig.txt',
    'uninstall.txt',
    'widget.txt',
    'transform_uids.txt',
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'tests/{0}'.format(test_file),
                package='collective.ckeditor',
                optionflags=OPTIONFLAGS,
            ),
            layer=CKEDITOR_FUNCTIONAL
        )
        for test_file in doc_tests
    ])

    return suite
