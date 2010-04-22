"""Common configuration constants
"""

PROJECTNAME = 'collective.ckeditor'

PROJECTTITLE = 'CKeditor for Plone'

I18NDOMAIN = 'collective.ckeditor'

# quintagroup.com (from qPloneResolveUID product)
RUID_URL_PATTERN = 'resolveuid' 
DOCUMENT_DEFAULT_OUTPUT_TYPE = "text/x-html-safe"
REQUIRED_TRANSFORM = "ck_ruid_to_url"
TAG_PATTERN = r'(\<(img|a|embed)[^>]*>)'
UID_PATTERN = r'(?P<uid_url>[^\"\']*%s/(?P<uid>[^\/\"\'#? ]*))' %RUID_URL_PATTERN