# Author: Melnychuk Taras
# Copyright: quintagroup.com

from zope.interface import implementer
import re
try:
    from Products.PortalTransforms.interfaces import ITransform
except ImportError:
    from Products.PortalTransforms.z3.interfaces import ITransform

from plone.app.uuid.utils import uuidToURL


def replace_resolveuid_urls_with_absolute_urls(text, compute_url=uuidToURL):
    tags_with_resolveuid, unique_uids = find_tags_with_resolveuid(text)
    if unique_uids:
        uid_to_absolute_url = make_uid_to_absolute_url(unique_uids, compute_url)
        for tag, uid, url in tags_with_resolveuid:
            if uid in uid_to_absolute_url:
                new_url = uid_to_absolute_url[uid]
                new_tag = tag.replace(url, new_url)
                text = text.replace(tag, new_tag)
    return text


TAG_WITH_URL_RE = r'(\<(img|a|embed)[^>]*>)'
TAG_WITH_URL = re.compile(TAG_WITH_URL_RE, re.I | re.S)

TAG_WITH_STYLE_RE = r'(\<[^>]*style=[^>]*url\([^>]*>)'
TAG_WITH_STYLE = re.compile(TAG_WITH_STYLE_RE, re.I | re.S)

RUID_URL = 'resolveuid'

RUID_URL_BETWEEN_QUOTES_RE = (
    r'(?P<url_with_uid>[^\"\']*%s/(?P<uid>[^\/\"\'#? ]*))' % RUID_URL
    )
RUID_URL_BETWEEN_QUOTES = re.compile(RUID_URL_BETWEEN_QUOTES_RE, re.I | re.S)

RUID_URL_BETWEEN_PARENS_RE = (
    r'[^(]*\((?P<url_with_uid>[^\"\')]*%s/(?P<uid>[^\/\"\')#? ]*))' % RUID_URL
    )
RUID_URL_BETWEEN_PARENS = re.compile(RUID_URL_BETWEEN_PARENS_RE, re.I | re.S)


def find_tags_with_resolveuid(data):
    tags_with_resolveuid = []
    unique_uids = set()

    for m in TAG_WITH_URL.finditer(data):
        ruid = re.search(RUID_URL_BETWEEN_QUOTES, m.group(0)[:3000])
        if ruid:
            tags_with_resolveuid.append(
                (m.group(0), ruid.group('uid'), ruid.group('url_with_uid'))
            )

    for m in TAG_WITH_STYLE.finditer(data):
        ruid = re.search(RUID_URL_BETWEEN_PARENS, m.group(0)[:3000])
        if ruid:
            tags_with_resolveuid.append(
                (m.group(0), ruid.group('uid'), ruid.group('url_with_uid'))
            )

    for tu in tags_with_resolveuid:
        unique_uids.add(tu[1])
    return tags_with_resolveuid, unique_uids


def make_uid_to_absolute_url(unique_uids, compute_url=uuidToURL):
    uid_to_absolute_url = {}
    for uid in unique_uids:
        url = compute_url(uid)
        if url is not None:
            uid_to_absolute_url[uid] = url
    return uid_to_absolute_url


@implementer(ITransform)
class ck_ruid_to_url:
    """Transform which replaces resolve uid in absolute urls"""

    __name__ = "ck_ruid_to_url"
    inputs = ('text/html',)
    output = 'text/html'

    def __init__(self, name=None):
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        converted = replace_resolveuid_urls_with_absolute_urls(orig)
        data.setData(converted)
        return data


def register():
    return ck_ruid_to_url()
