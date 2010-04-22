# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2006-08-11 
# Copyright: quintagroup.com

from zope.interface import implements
import re
from Products.CMFCore.utils import getToolByName
try:
    from Products.PortalTransforms.interfaces import ITransform
except ImportError:
    from Products.PortalTransforms.z3.interfaces import ITransform

from Products.PortalTransforms.interfaces import itransform

from collective.ckeditor.config import RUID_URL_PATTERN, TAG_PATTERN, UID_PATTERN

class ck_ruid_to_url:
    """Transform which replaces resolve uid in absolute urls"""

    implements(ITransform)    
    __implements__ = itransform
    
    __name__ = "ck_ruid_to_url"
    inputs  = ('text/html',)
    output = 'text/html'
    
    def __init__(self, name=None):
        if name:
            self.__name__ = name
        self.tag_regexp = re.compile(TAG_PATTERN ,re.I|re.S)
        self.ruid_regexp = re.compile(UID_PATTERN ,re.I|re.S)

    def name(self):
        return self.__name__

    def find_ruid(self, data):
        tags_ruid = []
        unique_ruid = []
        for m in self.tag_regexp.finditer(data):
            ruid = re.search(self.ruid_regexp, m.group(0))
            if ruid:
                tags_ruid.append((m.group(0), ruid.group('uid'), ruid.group('uid_url')))
        [unique_ruid.append(tu[1]) for tu in tags_ruid if tu[1] not in unique_ruid]
        return tags_ruid, unique_ruid

    def mapRUID_URL(self, unique_ruid, portal):
        ruid_url = {}
        rc = getToolByName(portal, 'reference_catalog')
        for uid in unique_ruid:
            obj = rc.lookupObject(uid)
            if obj is not None:
                ruid_url[uid] = obj.absolute_url()
        return ruid_url           
    
    def convert(self, orig, data, **kwargs):
        text = orig
        tags_ruid, unique_ruid = self.find_ruid(text)
        if unique_ruid:
            ruid_url = self.mapRUID_URL(unique_ruid, kwargs['context'])
            for tag_ruid in tags_ruid:
                t, uid, uid_url = tag_ruid
                if ruid_url.has_key(uid):                   
                    text = text.replace(t, t.replace(uid_url, ruid_url[uid]))
        
        data.setData(text)
        return data


def register():
    return ck_ruid_to_url()
    
