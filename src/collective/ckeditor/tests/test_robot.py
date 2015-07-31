from plone.testing import layered

import robotsuite

from ..testing import CKEDITOR_ROBOT


def test_suite():
    return layered(
        robotsuite.RobotTestSuite('robot/base.robot'),
        layer=CKEDITOR_ROBOT
    )
