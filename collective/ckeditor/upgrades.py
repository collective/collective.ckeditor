from Products.CMFCore.utils import getToolByName
PROFILE = "profile-collective.ckeditor:default"


def common_upgrade(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE)
