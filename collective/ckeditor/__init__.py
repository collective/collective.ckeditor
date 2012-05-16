from zope.i18nmessageid import MessageFactory
import config

import logging

LOG = logging.getLogger(config.PROJECTTITLE)

siteMessageFactory = MessageFactory(config.I18NDOMAIN)


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
