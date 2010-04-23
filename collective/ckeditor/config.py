"""Common configuration constants
"""

PROJECTNAME = 'collective.ckeditor'

PROJECTTITLE = 'CKeditor for Plone'

I18NDOMAIN = 'collective.ckeditor'

# the default toolbar used by CKEditor
CKEDITOR_PLONE_DEFAULT_TOOLBAR = """[
    ['Source','-','Save','Preview','-','Templates'],
    ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print', 'SpellChecker', 'Scayt'],
    ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
    ['Styles','Format','Font','FontSize'],
    '/',
    ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
    ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
    ['Link','Unlink','Anchor'],
    ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
    ['Maximize', 'ShowBlocks','-','About']
]"""

# quintagroup.com (from qPloneResolveUID product)
RUID_URL_PATTERN = 'resolveuid' 
DOCUMENT_DEFAULT_OUTPUT_TYPE = "text/x-html-safe"
REQUIRED_TRANSFORM = "ck_ruid_to_url"
TAG_PATTERN = r'(\<(img|a|embed)[^>]*>)'
UID_PATTERN = r'(?P<uid_url>[^\"\']*%s/(?P<uid>[^\/\"\'#? ]*))' %RUID_URL_PATTERN