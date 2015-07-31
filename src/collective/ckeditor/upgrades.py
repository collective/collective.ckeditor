from Products.CMFCore.utils import getToolByName


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
