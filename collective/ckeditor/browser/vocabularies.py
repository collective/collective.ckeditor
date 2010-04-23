# -*- coding: utf-8 -*-
## Copyright (C) 2009 Ingeniweb - all rights reserved    

""" Vocabularies used by control panel or widget
"""

from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.app.component.hooks import getSite
from Products.ATContentTypes.interfaces import IFileContent, IImageContent
from Products.Archetypes.interfaces.base import IBaseFolder
from Products.CMFCore.utils import getToolByName

from collective.ckeditor import siteMessageFactory as _

def _listTypesForInterface(portal, interface):
    """
    List of portal types that have File interface
    @param portal: plone site
    @param interface: Zope 2 inteface
    @return: [{'portal_type': xx, 'type_ui_info': UI type info}, ...]
    """
 
    archetype_tool = getToolByName(portal, 'archetype_tool')
    portal_types = getToolByName(portal, 'portal_types')
    utranslate = portal.utranslate
    
    # all_types = [{'name': xx, 'package': xx, 'portal_type': xx, 'module': xx,
    #               'meta_type': xx, 'klass': xx, ...
    all_types = archetype_tool.listRegisteredTypes(inProject=True)
    all_types = [tipe['portal_type'] for tipe in all_types
                 if interface.implementedBy(tipe['klass'])]
    # fix for bug in listRegisteredTypes which returns 2 'ATFolder'
    # when asking for IBaseFolder interface
    unik_types = dict.fromkeys(all_types).keys() 
    return [_infoDictForType(tipe, portal_types, utranslate) for tipe in unik_types]
    
def _infoDictForType(ptype, portal_types, utranslate):
    """
    UI type infos
    @param ptype: a portal type name
    @param portal_types: the portal_types tool
    @param utranslate: the translation func
    @return: {'portal_type': xxx, 'type_ui_info': UI type info}
    """
 
    type_info = getattr(portal_types, ptype)
    title = type_info.Title()
    product = type_info.product
    type_ui_info = ("%s (portal type: %s, product: %s)" %
                    (utranslate(title, default=title), ptype, product))
    return {
        'portal_type': ptype,
        'type_ui_info': type_ui_info
        }    

class CKEditorToolBarVocabulary(object):
    """Vocabulary factory for ckeditor toolbar
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [SimpleTerm('Basic', 'Basic', _(u'Minimal toolbar')),
                 SimpleTerm('Plone', 'Plone', _(u'Standard Plone toolbar (recommanded)')),
                 SimpleTerm('Custom', 'Custom', _(u'Custom Toolbar fill next field'))]
        return SimpleVocabulary(items)        


CKEditorToolBarVocabularyFactory = CKEditorToolBarVocabulary()

class CKEditorFileTypesVocabulary(object):
    """Vocabulary factory for ckeditor file types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        flt = _listTypesForInterface(portal, IFileContent)
        items = [ SimpleTerm(t['portal_type'], t['portal_type'], t['type_ui_info'])
                  for t in flt ]
        return SimpleVocabulary(items)
        
CKEditorFileTypesVocabularyFactory = CKEditorFileTypesVocabulary()        

class CKEditorUploadFileTypeVocabulary(object):
    """Vocabulary factory for ckeditor file type upload
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        flt = _listTypesForInterface(portal, IFileContent)
        items = [SimpleTerm('auto', 'auto', _(u'Content Type Registry default configuration (recommanded)')),
                 SimpleTerm('custom', 'custom', _(u'Custom configuration fill next field'))]
        items.extend([ SimpleTerm(t['portal_type'], t['portal_type'], t['type_ui_info'])
                  for t in flt ])
        return SimpleVocabulary(items)        
        

CKEditorUploadFileTypeVocabularyFactory = CKEditorUploadFileTypeVocabulary()

class CKEditorImageTypesVocabulary(object):
    """Vocabulary factory for ckeditor image types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        flt = _listTypesForInterface(portal, IImageContent)
        items = [ SimpleTerm(t['portal_type'], t['portal_type'], t['type_ui_info'])
                  for t in flt ]
        return SimpleVocabulary(items)

CKEditorImageTypesVocabularyFactory = CKEditorImageTypesVocabulary()

class CKEditorUploadImageTypeVocabulary(object):
    """Vocabulary factory for ckeditor image type upload
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        flt = _listTypesForInterface(portal, IImageContent)
        items = [SimpleTerm('auto', 'auto', _(u'Content Type Registry default configuration (recommanded)')),
                 SimpleTerm('custom', 'custom', _(u'Custom configuration, fill next field'))]
        items.extend([ SimpleTerm(t['portal_type'], t['portal_type'], t['type_ui_info'])
                  for t in flt ])
        return SimpleVocabulary(items)        
        

CKEditorUploadImageTypeVocabularyFactory = CKEditorUploadImageTypeVocabulary()

class CKEditorFolderTypesVocabulary(object):
    """Vocabulary factory for ckeditor folder types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        flt = _listTypesForInterface(portal, IBaseFolder)
        items = [SimpleTerm('custom', 'custom', _(u'Custom configuration, fill next field'))]
        items.extend([ SimpleTerm(t['portal_type'], t['portal_type'], t['type_ui_info'])
                  for t in flt ])
        return SimpleVocabulary(items)

CKEditorFolderTypesVocabularyFactory = CKEditorFolderTypesVocabulary()