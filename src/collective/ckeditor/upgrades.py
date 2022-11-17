from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone import api

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
        props.skin
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.toolbar",
        props.toolbar
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.toolbar_Custom",
        safe_unicode(props.toolbar_Custom)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.filtering",
        safe_unicode(props.filtering)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.customAllowedContent",
        safe_unicode(props.customAllowedContent)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.extraAllowedContent",
        safe_unicode(props.extraAllowedContent)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.disallowedContent",
        safe_unicode(props.disallowedContent)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.menuStyles",
        safe_unicode(props.menuStyles)
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.plugins",
        list(map(safe_unicode, props.plugins))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.removePlugins",
        list(map(safe_unicode, props.removePlugins))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.customTemplates",
        list(map(safe_unicode, props.customTemplates))
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
        props.bodyId
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.bodyClass",
        props.bodyClass
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.defaultTableWidth",
        props.defaultTableWidth
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.width",
        props.width
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.height",
        props.height
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
        props.file_portal_type
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.file_portal_type_custom",
        list(map(safe_unicode, props.file_portal_type_custom))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image_portal_type",
        props.image_portal_type
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image_portal_type_custom",
        list(map(safe_unicode, props.image_portal_type_custom))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.browse_images_portal_types",
        tuple(map(safe_unicode, props.browse_images_portal_types))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.flash_portal_type",
        props.flash_portal_type
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.flash_portal_type_custom",
        list(map(safe_unicode, props.flash_portal_type_custom))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.browse_flashs_portal_types",
        tuple(map(safe_unicode, props.browse_flashs_portal_types))
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.folder_portal_type",
        props.folder_portal_type
    )

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.folder_portal_type_custom",
        list(map(safe_unicode, props.folder_portal_type_custom))
    )

    # not migrating ck_force_path, ck_force_other_path, ck_force_root and ck_force_other_root because they are removed from the registry

    api.portal.set_registry_record(
        "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.overloadable_properties",
        list(props.properties_overloaded)
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
        props.image2_captionedClass
    )

    ptool.manage_delObjects("ckeditor_properties")
