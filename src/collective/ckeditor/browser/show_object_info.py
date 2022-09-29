from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse, NotFound
from zope.publisher.browser import BrowserView
import plone.api
import json

from plone.outputfilters.browser.resolveuid import uuidToURL


class ShowObjectInfoView(BrowserView):
    """For requests like /show_object_info/<uuid> return the normalized URL and Title.
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
        self.context.REQUEST.response.setHeader("Content-type", "application/json")
        obj = plone.api.content.get(UID=self.uuid)

        return json.dumps({
            'url': uuidToURL(self.uuid),
            'title': obj.Title() if obj else None,
        })
