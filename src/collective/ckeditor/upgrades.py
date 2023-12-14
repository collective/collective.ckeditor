from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone import api
import sys
from collective.ckeditor.setuphandlers import unregisterTransform
from collective.ckeditor.setuphandlers import unregisterTransformPolicy


PROFILE = "profile-collective.ckeditor:default"


def common_upgrade(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE)


def up3411(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if not props.hasProperty('plugins'):
        props.manage_addProperty(
            'plugins',
            ["ajaxsave;/++resource++cke_ajaxsave/plugin.js"],
            'list')


def up3612(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if not props.hasProperty('enableScaytOnStartup'):
        props.manage_addProperty(
            'enableScaytOnStartup',
            False,
            'boolean')


def up4000(context):
    jstool = getToolByName(context, 'portal_javascripts')
    jstool.manage_removeScript('++resource++ckeditor/ckeditor_basic.js')
    jstool.cookResources()
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE, 'jsregistry')


def up4001(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if not props.hasProperty('extraAllowedContent'):
        props.manage_addProperty(
            'extraAllowedContent',
            '/* Add items to array of allowedContent rules */\n[]',
            'text')


def up4002(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if not props.hasProperty('customAllowedContent'):
        props.manage_addProperty(
            'customAllowedContent',
            '/* Add items to array of allowedContent rules */\n[]',
            'text')
    if not props.hasProperty('filtering'):
        props.manage_addProperty(
            'filtering',
            'default',
            'string')


def up4300(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if not props.hasProperty('removePlugins'):
        props.manage_addProperty(
            'removePlugins',
            '',
            'lines')
    if not props.hasProperty('image2_alignClasses'):
        props.manage_addProperty(
            'image2_alignClasses',
            ['image-left', '', 'image-right'],
            'lines')
    if not props.hasProperty('image2_captionedClass'):
        props.manage_addProperty(
            'image2_captionedClass',
            "image",
            'string')


def up4301(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if not props.hasProperty('defaultTableWidth'):
        props.manage_addProperty(
            'defaultTableWidth',
            '500px',
            'string'
        )


def up4310(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if props.hasProperty('image2_alignClasses'):
        value = props.getProperty('image2_alignClasses')
        fixed = [item or 'image-dummy' for item in value]
        props.manage_changeProperties(image2_alignClasses=fixed)


def up4340(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties
    if props.hasProperty('plugins'):
        fixed = list(props.getProperty('plugins'))
        fixed.append("uploadwidget;/++resource++ckeditor/plugins/uploadwidget/plugin.js")
        fixed.append("uploadimage;/++resource++ckeditor/plugins/uploadimage/plugin.js")
        props.manage_changeProperties(plugins=fixed)


def to_registry(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.ckeditor_properties

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.forcePasteAsPlainText",
        props.forcePasteAsPlainText
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.skin",
        safe_string(props.skin)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.toolbar",
        safe_string(props.toolbar)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.toolbar_Custom",
        safe_string(props.toolbar_Custom)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.filtering",
        safe_string(props.filtering)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.customAllowedContent",
        safe_string(props.customAllowedContent)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.extraAllowedContent",
        safe_string(props.extraAllowedContent)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.disallowedContent",
        safe_string(props.disallowedContent)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.menuStyles",
        safe_unicode(props.menuStyles)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.plugins",
        list(map(safe_string, props.plugins))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.removePlugins",
        list(map(safe_string, props.removePlugins))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.customTemplates",
        list(map(safe_string, props.customTemplates))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.templatesReplaceContent",
        props.templatesReplaceContent
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.enableScaytOnStartup",
        props.enableScaytOnStartup
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.bodyId",
        safe_string(props.bodyId)
    )
    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.bodyClass",
        safe_string(props.bodyClass)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.defaultTableWidth",
        safe_string(props.defaultTableWidth)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.width",
        safe_string(props.width)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.height",
        safe_string(props.height)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_link_byuid",
        props.allow_link_byuid
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_relative_links",
        props.allow_relative_links
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_server_browsing",
        props.allow_server_browsing
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_file_upload",
        props.allow_file_upload
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_image_upload",
        props.allow_image_upload
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_flash_upload",
        props.allow_flash_upload
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.allow_folder_creation",
        props.allow_folder_creation
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.file_portal_type",
        safe_string(props.file_portal_type)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.file_portal_type_custom",
        list(map(safe_string, props.file_portal_type_custom))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image_portal_type",
        safe_string(props.image_portal_type)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image_portal_type_custom",
        list(map(safe_string, props.image_portal_type_custom))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.browse_images_portal_types",
        tuple(map(safe_string, props.browse_images_portal_types))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.flash_portal_type",
        safe_string(props.flash_portal_type)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.flash_portal_type_custom",
        list(map(safe_string, props.flash_portal_type_custom))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.browse_flashs_portal_types",
        tuple(map(safe_string, props.browse_flashs_portal_types))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.folder_portal_type",
        safe_string(props.folder_portal_type)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.folder_portal_type_custom",
        list(map(safe_string, props.folder_portal_type_custom))
    )

    # not migrating ck_force_path, ck_force_other_path, ck_force_root and ck_force_other_root because they are removed from the registry
    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.overloadable_properties",
        list(map(safe_string, props.properties_overloaded))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.entities",
        props.entities
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.entities_greek",
        props.entities_greek
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.entities_latin",
        props.entities_latin
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image2_alignClasses",
        list(props.image2_alignClasses)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image2_captionedClass",
        safe_string(props.image2_captionedClass)
    )

    ptool.manage_delObjects("ckeditor_properties")


IS_PYTHON2 = sys.version_info[0] == 2
if IS_PYTHON2:
    text_type = unicode
    binary_type = str
    string_none = "None"
else:
    text_type = str
    binary_type = bytes
    string_none = b"None"


def safe_string(value):
    if value is None:
        return binary_type()
    if isinstance(value, text_type):
        result = value.encode('utf8')
    else:
        result = value
    # workaround old settings screen that stored empty input as "None" string
    if result == string_none:
        return binary_type()
    else:
        return result


DOCUMENT_DEFAULT_OUTPUT_TYPE = "text/x-html-safe"
REQUIRED_TRANSFORM = "ck_ruid_to_url"


def no_transform(context):
    site = api.portal.get()
    unregisterTransform(site, 'ck_ruid_to_url')
    unregisterTransformPolicy(site, DOCUMENT_DEFAULT_OUTPUT_TYPE,
                              REQUIRED_TRANSFORM)
