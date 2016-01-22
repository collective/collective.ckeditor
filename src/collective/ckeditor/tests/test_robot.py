from plone.testing import layered

import robotsuite
import unittest

from ..testing import CKEDITOR_ROBOT
from ..testing import CKEDITOR_SCAYT_ROBOT
from ..testing import CKEDITOR_IMAGE2_ROBOT


def test_suite():
    return unittest.TestSuite(
        [
            layered(
                robotsuite.RobotTestSuite('robot/base.robot'),
                layer=CKEDITOR_ROBOT
            ),
            layered(
                robotsuite.RobotTestSuite('robot/scayt.robot'),
                layer=CKEDITOR_SCAYT_ROBOT
            ),
            layered(
                robotsuite.RobotTestSuite('robot/image2.robot'),
                layer=CKEDITOR_IMAGE2_ROBOT
            ),
        ]
    )
