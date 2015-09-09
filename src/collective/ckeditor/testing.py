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

CKEDITOR_ROBOT = FunctionalTesting(
    bases=(CKEDITOR, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CKEDITOR_ROBOT',
)
