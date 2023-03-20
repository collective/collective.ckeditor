from plone.testing import layered

import robotsuite
import unittest

from ..testing import CKEDITOR_ROBOT
from ..testing import CKEDITOR_SCAYT_ROBOT
from ..testing import CKEDITOR_IMAGE2_ROBOT

import sys
if sys.version_info[0] >= 3:
    def test_suite():
        return unittest.TestSuite(
            [
                layered(
                    robotsuite.RobotTestSuite('robot/base.robot'),
                    layer=CKEDITOR_ROBOT
                ),
                layered(
                    robotsuite.RobotTestSuite('robot/staticportlet.robot'),
                    layer=CKEDITOR_ROBOT
                ),
    # Disabled because CORS errors in Firefox
    #            layered(
    #                robotsuite.RobotTestSuite('robot/scayt.robot'),
    #                layer=CKEDITOR_SCAYT_ROBOT
    #            ),
                layered(
                    robotsuite.RobotTestSuite('robot/image2.robot'),
                    layer=CKEDITOR_IMAGE2_ROBOT
                ),
            ]
        )
else:
    def test_suite():
        return unittest.TestSuite(
            [
                layered(
                    robotsuite.RobotTestSuite('robot/base-py27.robot'),
                    layer=CKEDITOR_ROBOT
                ),
                layered(
                    robotsuite.RobotTestSuite('robot/image2-py27.robot'),
                    layer=CKEDITOR_IMAGE2_ROBOT
                ),
            ]
        )
