from collective.ckeditor import LOG
from collective.ckeditor.config import DOCUMENT_DEFAULT_OUTPUT_TYPE, REQUIRED_TRANSFORM
from Products.CMFPlone.utils import getToolByName


def importFinalSteps(context):

    if context.readDataFile('collective.ckeditor.txt') is None:
        return
    site = context.getSite()
    registerTransform(site, 'ck_ruid_to_url', 'collective.ckeditor.transforms.ck_ruid_to_url')
    registerTransformPolicy(site, DOCUMENT_DEFAULT_OUTPUT_TYPE, REQUIRED_TRANSFORM)
    LOG.info('CKEditor for Plone installed')

def uninstallSteps(context) :
    if context.readDataFile('collective.ckeditor.uninstall.txt') is None:
        return
    site = context.getSite()
    uninstallControlPanel(site)
    uninstallSiteProperties(site)
    unregisterTransform(site, 'ck_ruid_to_url')
    unregisterTransformPolicy(site, DOCUMENT_DEFAULT_OUTPUT_TYPE, REQUIRED_TRANSFORM)
    LOG.info('CKEditor for Plone uninstalled')

def registerTransform(context, name, module):
    transforms = getToolByName(context, 'portal_transforms')
    if name not in transforms.objectIds() :
        transforms.manage_addTransform(name, module)
        LOG.info("Registered transform '%s'" %name)
    else :
        LOG.info("Transform '%s' always registered" %name)

def registerTransformPolicy(context, output_mimetype, required_transform):
    transforms = getToolByName(context, 'portal_transforms')
    tpolicies = transforms.listPolicies()
    mimetype_registered = False
    for p in tpolicies :
        out_type = p[0]
        if out_type==output_mimetype :
            policies = list(p[1])
            if required_transform not in policies :
                policies.append(required_transform) 
                transforms.manage_delPolicies([output_mimetype])
                transforms.manage_addPolicy(output_mimetype, policies)
            mimetype_registered = True
            break
    if not mimetype_registered :
        transforms.manage_addPolicy(output_mimetype, [required_transform])
    LOG.info("Registered policy for '%s' mimetype" %output_mimetype) 

def uninstallControlPanel(context):
    """
    Uninstall CKeditor control panel
    Since the xml uninstall profile does not work
    """
    controlpanel = getToolByName(context, 'portal_controlpanel')
    controlpanel.unregisterConfiglet(id='CKEditor')
    LOG.info("CKEditor configlet removed") 

def uninstallSiteProperties(context) :
    """
    Remove CKeditor as available editor
    could not be done with GS
    Remark : we don' t change the default editor
    (the ckeditor installer do not change it)
    """
    ptool = getToolByName(context, 'portal_properties')
    stp = ptool.site_properties
    ae = list(stp.getProperty('available_editors'))
    if 'CKeditor' in ae :
        ae.remove('CKeditor')
        stp.manage_changeProperties(REQUEST=None, available_editors = ae)
    
def unregisterTransform(context, name):
    transforms = getToolByName(context, 'portal_transforms')
    if name in transforms.objectIds() :
        transforms.unregisterTransform(name)
        LOG.info("Removed transform '%s'" %name) 
    else :
        LOG.info("Transform '%s' was not registered" %name)

def unregisterTransformPolicy(context, output_mimetype, required_transform):
    transforms = getToolByName(context, 'portal_transforms')
    tpolicies = transforms.listPolicies()
    for p in tpolicies :
        out_type = p[0]
        if out_type==output_mimetype :
            policies = list(p[1])
            if required_transform in policies :
                policies.remove(required_transform) 
                transforms.manage_delPolicies([output_mimetype])
                if policies :
                    transforms.manage_addPolicy(output_mimetype, policies)
            break
    LOG.info("Removed transform policy for '%s' mimetype" %output_mimetype)

