from Products.CMFCore.utils import getToolByName


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    profile = 'profile-collective.ckeditor:uninstall'
    setup_tool.runAllImportStepsFromProfile(profile)
    return "CKeditor for Plone uninstalled."
