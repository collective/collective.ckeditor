"""Common configuration constants
"""

PROJECTNAME = 'collective.ckeditor'

PROJECTTITLE = 'CKeditor for Plone'

I18NDOMAIN = 'collective.ckeditor'

# the default toolbar used by CKEditor
CKEDITOR_PLONE_DEFAULT_TOOLBAR = """[
    ['Source','-','AjaxSave','Preview','-','Templates'],
    ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print',
    'SpellChecker', 'Scayt'],
    ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
    ['Styles','Format','Font','FontSize'],
    '/',
    ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
    ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
    ['Link','Unlink','Anchor'],
    ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar',
    'PageBreak'],
    ['Maximize', 'ShowBlocks','-','About']
]"""

CKEDITOR_BASIC_TOOLBAR = """[
    ['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-',
    'Link', 'Unlink','-','About']
]"""

# the full feautured CKeditor toolbar
CKEDITOR_FULL_TOOLBAR = """[
    ['Source','-','AjaxSave','Preview','-','Templates'],
    ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print',
    'SpellChecker', 'Scayt'],
    ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
    ['Styles','Format','Font','FontSize','TextColor','BGColor'],
    '/',
    ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
    ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote','CreateDiv'],
    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','BidiLtr','BidiRtl'],
    ['Link','Unlink','Anchor'],
    ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar',
    'PageBreak','Iframe'],
    ['Maximize', 'ShowBlocks','-','About']
]"""

CKEDITOR_BASIC_TOOLBAR = """[
            ['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-',
                'Link', 'Unlink','-','About']
]"""

# XXX warning order language correctly because if several values for the same
# main language, the first defined language will be used as fallback when
# trying to find SCAYT language to use when enableScaytOnStartup is True
CKEDITOR_SUPPORTED_LANGUAGE_CODES = (
    'da_DK',
    'de_DE',
    'es_ES',
    'el_GR',
    'en_US', 'en_CA', 'en_GB',
    'fr_FR', 'fr_CA',
    'fi_FI',
    'it_IT',
    'nb_NO',
    'nl_NL',
    'pt_PT', 'pt_BR',
    'sv_SE', )
