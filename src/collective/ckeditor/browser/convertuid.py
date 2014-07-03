from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.browser import BrowserView

from plone.outputfilters.browser.resolveuid import uuidToURL


class ConvertUIDView(BrowserView):
    """Resolve a URL like /convert_uid_to_url/<uuid> to a normalized URL.
    """
    implements(IPublishTraverse)

    subpath = None

    def publishTraverse(self, request, name):
        self.uuid = name
        traverse_subpath = self.request['TraversalRequestNameStack']
        if traverse_subpath:
            traverse_subpath = list(traverse_subpath)
            traverse_subpath.reverse()
            self.subpath = traverse_subpath
            self.request['TraversalRequestNameStack'] = []
        return self

    def __call__(self):
        return uuidToURL(self.uuid)
