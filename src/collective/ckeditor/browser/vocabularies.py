# -*- coding: utf-8 -*-

""" Vocabularies used by control panel or widget
"""

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    from zope.app.schema.vocabulary import IVocabularyFactory

from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

try:
    from Products.ATContentTypes.interfaces import IFileContent, IImageContent
    from Products.Archetypes.interfaces.base import IBaseFolder
    HAS_AT = True
except ImportError:
    HAS_AT = False

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
    types = archetype_tool.listPortalTypesWithInterfaces([interface])
    all_types = [tipe.getId() for tipe in types]
    # fix for bug in listPortalTypesWithInterfaces which returns 2 'ATFolder'
    # when asking for IBaseFolder interface
    unik_types = dict.fromkeys(all_types).keys()
    return [_infoDictForType(tipe, portal_types, utranslate)
            for tipe in unik_types]


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


@implementer(IVocabularyFactory)
class CKEditorSkinVocabulary(object):
    """Vocabulary factory for ckeditor skin
    """

    def __call__(self, context):
        items = [SimpleTerm('moonocolor', 'moonocolor',
                            _(u'Colored buttons')),
                 SimpleTerm('moono-lisa', 'moono-lisa',
                            _(u'Flat buttons'))]
        return SimpleVocabulary(items)

CKEditorSkinVocabularyFactory = CKEditorSkinVocabulary()


@implementer(IVocabularyFactory)
class CKEditorToolBarVocabulary(object):
    """Vocabulary factory for ckeditor toolbar
    """

    def __call__(self, context):
        items = [SimpleTerm('Basic', 'Basic',
                            _(u'Minimal toolbar')),
                 SimpleTerm('Full', 'Full',
                            _(u'Full CKeditor toolbar providing every '
                              u'available functionnalities (some '
                              u'functionnalities could not work correctly '
                              u'depending on your Plone settings)')),
                 SimpleTerm('Plone', 'Plone',
                            _(u'Standard Plone toolbar (recommanded)')),
                 SimpleTerm('Custom', 'Custom',
                            _(u'Custom Toolbar fill next field'))]
        return SimpleVocabulary(items)

CKEditorToolBarVocabularyFactory = CKEditorToolBarVocabulary()


@implementer(IVocabularyFactory)
class CKEditorFilteringVocabulary(object):
    """Vocabulary factory for ckeditor filtering
    """

    def __call__(self, context):
        items = [SimpleTerm('default', 'Based on UI',
                            _(u'Automatic')),
                 SimpleTerm('disabled', 'Disabled',
                            _(u'Disabled: any content is allowed.')),
                 SimpleTerm('custom', 'Custom filtering',
                            _(u'Custom: filter is setup according to '
                              u'Custom Allowed Content option.'))]
        return SimpleVocabulary(items)

CKEditorFilteringVocabularyFactory = CKEditorFilteringVocabulary()


@implementer(IVocabularyFactory)
class CKEditorFileTypesVocabulary(object):
    """Vocabulary factory for ckeditor file types
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        if HAS_AT:
            flt = _listTypesForInterface(portal, IFileContent)
            items = [SimpleTerm(t['portal_type'], t['portal_type'],
                                t['type_ui_info'])
                     for t in flt]
        else:
            # TODO compute from actual portal_types
            items = [
                     SimpleTerm('File', 'File', _(u'File'))]
        return SimpleVocabulary(items)

CKEditorFileTypesVocabularyFactory = CKEditorFileTypesVocabulary()


@implementer(IVocabularyFactory)
class CKEditorUploadFileTypeVocabulary(object):
    """Vocabulary factory for ckeditor file type upload
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        if HAS_AT:
            flt = _listTypesForInterface(portal, IFileContent)
            msg1 = _(u'Content Type Registry default configuration (recommanded)')
            msg2 = _(u'Custom configuration, fill next field')
            items = [SimpleTerm('auto', 'auto', msg1),
                     SimpleTerm('custom', 'custom', msg2)]
            items.extend([SimpleTerm(t['portal_type'], t['portal_type'],
                                     t['type_ui_info'])
                          for t in flt])
        else:
            # TODO compute from actual portal_types
            msg1 = _(u'Content Type Registry default configuration (recommanded)')
            msg2 = _(u'Custom configuration, fill next field')
            items = [SimpleTerm('auto', 'auto', msg1),
                     SimpleTerm('custom', 'custom', msg2)]
            items.extend([
                     SimpleTerm('File', 'File', _(u'File'))])
        return SimpleVocabulary(items)

CKEditorUploadFileTypeVocabularyFactory = CKEditorUploadFileTypeVocabulary()


@implementer(IVocabularyFactory)
class CKEditorImageTypesVocabulary(object):
    """Vocabulary factory for ckeditor image types
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        if HAS_AT:
            flt = _listTypesForInterface(portal, IImageContent)
            items = [SimpleTerm(t['portal_type'], t['portal_type'],
                                t['type_ui_info'])
                     for t in flt]
        else:
            # TODO compute from actual portal_types
            items = [
                     SimpleTerm('Image', 'Image', _(u'Image'))]
        return SimpleVocabulary(items)

CKEditorImageTypesVocabularyFactory = CKEditorImageTypesVocabulary()


@implementer(IVocabularyFactory)
class CKEditorUploadImageTypeVocabulary(object):
    """Vocabulary factory for ckeditor image type upload
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        if HAS_AT:
            flt = _listTypesForInterface(portal, IImageContent)
            msg1 = _(u'Content Type Registry default configuration (recommanded)')
            msg2 = _(u'Custom configuration, fill next field')
            items = [SimpleTerm('auto', 'auto', msg1),
                     SimpleTerm('custom', 'custom', msg2)]
            items.extend([SimpleTerm(t['portal_type'], t['portal_type'],
                                     t['type_ui_info'])
                          for t in flt])
        else:
            # TODO compute from actual portal_types
            msg1 = _(u'Content Type Registry default configuration (recommanded)')
            msg2 = _(u'Custom configuration, fill next field')
            items = [SimpleTerm('auto', 'auto', msg1),
                     SimpleTerm('custom', 'custom', msg2)]
            items.extend([
                     SimpleTerm('Image', 'Image', _(u'Image'))])
        return SimpleVocabulary(items)

CKEditorUploadImageTypeVocabularyFactory = CKEditorUploadImageTypeVocabulary()


@implementer(IVocabularyFactory)
class CKEditorFolderTypesVocabulary(object):
    """Vocabulary factory for ckeditor folder types
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        if HAS_AT:
            flt = _listTypesForInterface(portal, IBaseFolder)
            items = [SimpleTerm('custom', 'custom',
                                _(u'Custom configuration, fill next field'))]
            items.extend([SimpleTerm(t['portal_type'], t['portal_type'],
                                     t['type_ui_info'])
                          for t in flt])
        else:
            # TODO compute from actual portal_types
            items = [SimpleTerm('custom', 'custom',
                                _(u'Custom configuration, fill next field')),
                     SimpleTerm('Folder', 'Folder', _(u'Folder'))]
        return SimpleVocabulary(items)

CKEditorFolderTypesVocabularyFactory = CKEditorFolderTypesVocabulary()
