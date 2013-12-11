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
