from collective.ckeditor import LOG
from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import IBundleRegistry
from Products.CMFPlone.interfaces import IEditingSchema
from zope.interface import implementer
from zope.component import getUtility


def importFinalSteps(context):

    if context.readDataFile('collective.ckeditor.txt') is None:
        return
    site = context.getSite()
    LOG.info('CKEditor for Plone installed')


def uninstallSteps(context):
    if context.readDataFile('collective.ckeditor.uninstall.txt') is None:
        return
    site = context.getSite()
    uninstallControlPanel(site)
    uninstallFromRegistry(site)
    uninstallMemberProperties(site)
    LOG.info('CKEditor for Plone uninstalled')


def uninstallControlPanel(context):
    """
    Uninstall CKeditor control panel
    Since the xml uninstall profile does not work
    """
    controlpanel = getToolByName(context, 'portal_controlpanel')
    controlpanel.unregisterConfiglet(id='CKEditor')
    LOG.info("CKEditor configlet removed")


def uninstallFromRegistry(context):
    """
    Remove CKeditor as available editor.
    Could not be done with GS.
    If default editor is CKeditor, we change it to TinyMCE
    or the basic html area.
    """

    registry = getUtility(IRegistry)
    settings = registry.forInterface(
        IEditingSchema,
        prefix='plone',
        check=False
    )

    available_editors = settings.available_editors
    if 'CKeditor' in available_editors:
        available_editors.remove('CKeditor')
        settings.available_editors = available_editors

    if settings.default_editor == 'CKeditor':
        if 'TinyMCE' in available_editors:
            settings.default_editor='TinyMCE'
        else:
            # Basic HTML area
            settings.default_editor='None'

    for key in registry.records.keys():
        if key.startswith(
            "collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema"
        ):
            del registry.records[key]
        if key.startswith(
            "collective.ckeditor.toolbars"
        ):
            del registry.records[key]

    bundles = registry.collectionOfInterface(IBundleRegistry, prefix="plone.bundles")
    for name in bundles:
        if name.startswith("collective.ckeditor"):
            del bundles[name]


def uninstallMemberProperties(context):
    """
    Remove CKeditor as wysiwyg_editor for new members.

    We used to set this, but stopped doing so, in favour of the
    default_editor site property.  But we should undo it if this value
    is still used.
    """
    memberdata = getToolByName(context, 'portal_memberdata')
    wysiwyg_editor = memberdata.getProperty('wysiwyg_editor', '')
    if wysiwyg_editor == 'CKeditor':
        # Use the site default editor.
        memberdata.manage_changeProperties(REQUEST=None, wysiwyg_editor='')


def unregisterTransform(context, name):
    transforms = getToolByName(context, 'portal_transforms')
    if name in transforms.objectIds():
        transforms.unregisterTransform(name)
        LOG.info("Removed transform '%s'" % name)
    else:
        LOG.info("Transform '%s' was not registered" % name)


def unregisterTransformPolicy(context, output_mimetype, required_transform):
    transforms = getToolByName(context, 'portal_transforms')
    tpolicies = transforms.listPolicies()
    for p in tpolicies:
        out_type = p[0]
        if out_type == output_mimetype:
            policies = list(p[1])
            if required_transform in policies:
                policies.remove(required_transform)
                transforms.manage_delPolicies([output_mimetype])
                if policies:
                    transforms.manage_addPolicy(output_mimetype, policies)
            break
    LOG.info("Removed transform policy for '%s' mimetype" % output_mimetype)


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.ckeditor:uninstall",
            "collective.ckeditor:to4350",
            "collective.ckeditor:to4330",
            "collective.ckeditor:to5010",
        ]
