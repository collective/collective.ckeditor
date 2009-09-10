
from collective.ckeditor import LOG



def importFinalSteps(context):

    if context.readDataFile('collective.ckeditor.txt') is None:
        return
    #site = context.getSite()
    LOG.info('ckeditor for Plone installed')
    
                    
    
