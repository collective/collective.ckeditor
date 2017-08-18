from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

import collective.ckeditor


CKEDITOR = PloneWithPackageLayer(
    zcml_package=collective.ckeditor,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.ckeditor:testing',
    name='CKEDITOR',
)

CKEDITOR_INTEGRATION = IntegrationTesting(
    bases=(CKEDITOR, ),
    name='CKEDITOR_INTEGRATION',
)

CKEDITOR_FUNCTIONAL = FunctionalTesting(
    bases=(CKEDITOR, ),
    name='CKEDITOR_FUNCTIONAL',
)

CKEDITOR_ROBOT_BASE  = PloneWithPackageLayer(
    bases=(REMOTE_LIBRARY_BUNDLE_FIXTURE, ),
    zcml_package=collective.ckeditor,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.ckeditor:testing',
    name='CKEDITOR_ROBOT_BASE',
)

CKEDITOR_ROBOT = FunctionalTesting(
    bases=(CKEDITOR_ROBOT_BASE, z2.ZSERVER_FIXTURE),
    name='CKEDITOR_ROBOT',
)

CKEDITOR_SCAYT = PloneWithPackageLayer(
    bases=(REMOTE_LIBRARY_BUNDLE_FIXTURE, ),
    zcml_package=collective.ckeditor,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.ckeditor:testing_scayt',
    name='CKEDITOR_SCAYT',
)

CKEDITOR_SCAYT_ROBOT = FunctionalTesting(
    bases=(CKEDITOR_SCAYT, z2.ZSERVER_FIXTURE),
    name='CKEDITOR_SCAYT_ROBOT',
)

CKEDITOR_IMAGE2 = PloneWithPackageLayer(
    bases=(REMOTE_LIBRARY_BUNDLE_FIXTURE, ),
    zcml_package=collective.ckeditor,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.ckeditor:testing_image2',
    name='CKEDITOR_IMAGE2',
)

CKEDITOR_IMAGE2_ROBOT = FunctionalTesting(
    bases=(CKEDITOR_IMAGE2, z2.ZSERVER_FIXTURE),
    name='CKEDITOR_IMAGE2_ROBOT',
)
