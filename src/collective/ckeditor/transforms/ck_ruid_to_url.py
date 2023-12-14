from zope.interface import implementer
import re
try:
    from Products.PortalTransforms.interfaces import ITransform
except ImportError:
    from Products.PortalTransforms.z3.interfaces import ITransform


@implementer(ITransform)
class ck_ruid_to_url:
    """Dummy transform kept to enable uninstallation.
    Might be tottaly removed later.
    """

    __name__ = "ck_ruid_to_url"
    inputs = ('text/html',)
    output = 'text/html'

    def __init__(self, name=None):
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        data.setData(orig)
        return data


def register():
    return ck_ruid_to_url()
