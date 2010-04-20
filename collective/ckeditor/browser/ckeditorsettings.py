from Acquisition import aq_inner
from zope.interface import implements, Interface
from zope.component import adapts
from zope.app.component.hooks import getSite
from Products.Five import BrowserView

from zope.formlib.form import FormFields
from zope.schema import Bool
from zope.schema import Text
from zope.schema import TextLine
from zope.schema import SourceText
from zope.schema import Choice
from zope.schema import Tuple
from zope.schema import List

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.utils import safe_unicode

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from plone.locking.interfaces import ILockSettings

from collective.ckeditor import siteMessageFactory as _
from collective.ckeditor import LOG


class ICKEditorBrowserSchema(Interface):
    """
    CKEditor Browser fieldset schema
    """
    allow_link_byuid = Bool(title=_(u"Allow link objects by UID"),
                            description =_(u"Check if you want url with Unique ID "
                                            "(no more 404 errors when moving objects). "
                                            "Notice that portal_transforms in standard configuration "
                                            "transforms uid links in absolute urls "
                                            "in view displays."),
                            default = True,
                            required = False)

    allow_relative_links = Bool(title=_(u"Allow relative urls transformation"),
                                description=_(u"Check if you want relative urls after saving forms. "
                                               "Useful when link by uid is not checked. "),
                                default=False,
                                required=False)

    allow_server_browsing = Bool(title=_(u"Allow browsing for links"),
                                 description=_(u"Check to allow server browsing used for medias linking. "),
                                 default=True,
                                 required=False)

    allow_file_upload = Bool(title=_(u"Allow file upload"),
                             description=_(u"Check to allow files upload in link dialog boxes). "),
                             default=False,
                             required=False)

    allow_image_upload = Bool(title=_(u"Allow image upload"),
                              description=_(u"Check to allow upload for images. "),
                              default=False,
                              required=False)

    allow_flash_upload = Bool(title=_(u"Allow flash upload"),
                              description=_(u"Check to allow upload for flash content. "),
                              default=False,
                              required=False)

    allow_folder_creation = Bool(title=_(u"Allow folder creation"),
                                 description=_(u"Check to allow folder creation in browser. "),
                                 default=False,
                                 required=False)

    file_portal_type = Choice( title=_(u"File portal type"),
                               description=_(u"Choose the portal type used for file upload"),
                               required=True,
                               default='File',
                               vocabulary="collective.ckeditor.vocabularies.FileTypeUpload")
                               
    file_portal_type_custom = List( title=_(u"Custom File portal type for upload"),
                                    description=_(u"Add list of pairs CONTAINER_TYPE|FILE_TYPE. "
                                                   "The file portal type choosen for upload will depend on "
                                                   "contextual container portal type. "
                                                   "* means any portal type. "
                                                   "Take care, no control is done over this field value."),
                                    required=False,
                                    value_type=TextLine(),
                                    default=['*|File', 'Folder|File', ])           

    browse_images_portal_types = Tuple(title=_(u"Portal Types for images linking"),
                                       description=_(u"Choose the types used "
                                                      "for images selection in browser. "),
                                       required=True,
                                       missing_value=tuple(),
                                       default = ('Image','News Item',),
                                       value_type = Choice(
                                                    vocabulary="collective.ckeditor.vocabularies.ImageTypes"))

    image_portal_type = Choice( title=_(u"Image portal type"),
                               description=_(u"Choose the portal type used for image upload"),
                               required=True,
                               default='auto',
                               vocabulary="collective.ckeditor.vocabularies.ImageTypeUpload")
                               
    image_portal_type_custom = List( title=_(u"Custom Image portal type for upload"),
                                     description=_(u"Add list of pairs CONTAINER_TYPE|IMAGE_TYPE. "
                                                    "The image portal type choosen for upload will depend on "
                                                    "contextual container portal type. "
                                                   "* means any portal type. "
                                                    "Take care, no control is done over this field value."),
                                     required=False,
                                     value_type=TextLine(),
                                     default=['*|Image', 'Folder|Image', ])                               

    browse_flashs_portal_types = Tuple(title=_(u"Portal Types for flah contents linking"),
                                       description=_(u"Choose the types used "
                                                      "for flash contents selection in browser. "),
                                       required=True,
                                       missing_value=tuple(),
                                       default = ('File',),
                                       value_type = Choice(
                                                    vocabulary="collective.ckeditor.vocabularies.FileTypes"))

    flash_portal_type = Choice( title=_(u"Flash portal type"),
                                description=_(u"Choose the portal type used for flash content upload"),
                                required=True,
                                default='File',
                                vocabulary="collective.ckeditor.vocabularies.FileTypeUpload")
                               
    flash_portal_type_custom = List( title=_(u"Custom Flash portal type for upload"),
                                     description=_(u"Add list of pairs CONTAINER_TYPE|FLASH_TYPE. "
                                                    "The flash portal type choosen for upload will depend on "
                                                    "contextual container portal type. "
                                                   "* means any portal type. "
                                                    "Take care, no control is done over this field value."),
                                     required=False,
                                     value_type=TextLine(),
                                     default=['*|File', 'Folder|File', ])  

    folder_portal_type = Choice( title=_(u"Folder portal type"),
                                 description=_(u"Choose the portal type used for folder creation"),
                                 required=True,
                                 default='Folder',
                                 vocabulary="collective.ckeditor.vocabularies.FolderTypes")
                               
    folder_portal_type_custom = List( title=_(u"Custom portal type for folder creation"),
                                      description=_(u"Add list of pairs CONTAINER_TYPE|FOLDER_TYPE. "
                                                     "The folder portal type choosen for folders creation will depend on "
                                                     "contextual container portal type. "
                                                     "* means any portal type. "
                                                     "Take care, no control is done over this field value."),
                                     required=False,
                                     value_type=TextLine(),
                                     default=['*|Folder', 'Large Plone Folder|Large Plone Folder', ])

class ICKEditorSchema(ICKEditorBrowserSchema,):
    """Combined schema for the adapter lookup.
    """

class CKEditorControlPanelAdapter(SchemaAdapterBase):

    implements(ICKEditorSchema)
    adapts(IPloneSiteRoot)
    
    def __init__(self, context):
        super(CKEditorControlPanelAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.ckeditor_properties
        self.encoding = pprop.site_properties.default_charset

    def get_allow_link_byuid(self):
        return self.context.allow_link_byuid

    def set_allow_link_byuid(self, value):
        self.context._updateProperty('allow_link_byuid', value)

    allow_link_byuid = property(get_allow_link_byuid, set_allow_link_byuid)

    def get_allow_relative_links(self):
        return self.context.allow_relative_links

    def set_allow_relative_links(self, value):
        self.context._updateProperty('allow_relative_links', value)

    allow_relative_links = property(get_allow_relative_links, set_allow_relative_links)

    def get_allow_server_browsing(self):
        return self.context.allow_server_browsing

    def set_allow_server_browsing(self, value):
        self.context._updateProperty('allow_server_browsing', value)

    allow_server_browsing = property(get_allow_server_browsing, set_allow_server_browsing)

    def get_allow_file_upload(self):
        return self.context.allow_file_upload

    def set_allow_file_upload(self, value):
        self.context._updateProperty('allow_file_upload', value)

    allow_file_upload = property(get_allow_file_upload, set_allow_file_upload)

    def get_allow_image_upload(self):
        return self.context.allow_image_upload

    def set_allow_image_upload(self, value):
        self.context._updateProperty('allow_image_upload', value)

    allow_image_upload = property(get_allow_image_upload, set_allow_image_upload)

    def get_allow_flash_upload(self):
        return self.context.allow_flash_upload

    def set_allow_flash_upload(self, value):
        self.context._updateProperty('allow_flash_upload', value)

    allow_flash_upload = property(get_allow_flash_upload, set_allow_flash_upload)

    def get_allow_folder_creation(self):
        return self.context.allow_folder_creation

    def set_allow_folder_creation(self, value):
        self.context._updateProperty('allow_folder_creation', value)

    allow_folder_creation = property(get_allow_folder_creation, set_allow_folder_creation)

    def get_file_portal_type(self):
        return self.context.file_portal_type

    def set_file_portal_type(self, value):
        self.context._updateProperty('file_portal_type', value)

    file_portal_type = property(get_file_portal_type, set_file_portal_type)

    def get_file_portal_type_custom(self):
        return self.context.file_portal_type_custom

    def set_file_portal_type_custom(self, value):
        self.context._updateProperty('file_portal_type_custom', value)

    file_portal_type_custom = property(get_file_portal_type_custom, set_file_portal_type_custom)

    def get_browse_images_portal_types(self):
        return self.context.browse_images_portal_types

    def set_browse_images_portal_types(self, value):
        self.context._updateProperty('browse_images_portal_types', value)

    browse_images_portal_types = property(get_browse_images_portal_types, set_browse_images_portal_types)

    def get_image_portal_type(self):
        return self.context.image_portal_type

    def set_image_portal_type(self, value):
        self.context._updateProperty('image_portal_type', value)

    image_portal_type = property(get_image_portal_type, set_image_portal_type)

    def get_image_portal_type_custom(self):
        return self.context.image_portal_type_custom

    def set_image_portal_type_custom(self, value):
        self.context._updateProperty('image_portal_type_custom', value)

    image_portal_type_custom = property(get_image_portal_type_custom, set_image_portal_type_custom)

    def get_browse_flashs_portal_types(self):
        return self.context.browse_flashs_portal_types

    def set_browse_flashs_portal_types(self, value):
        self.context._updateProperty('browse_flashs_portal_types', value)

    browse_flashs_portal_types = property(get_browse_flashs_portal_types, set_browse_flashs_portal_types)

    def get_flash_portal_type(self):
        return self.context.flash_portal_type

    def set_flash_portal_type(self, value):
        self.context._updateProperty('flash_portal_type', value)

    flash_portal_type = property(get_flash_portal_type, set_flash_portal_type)

    def get_flash_portal_type_custom(self):
        return self.context.flash_portal_type_custom

    def set_flash_portal_type_custom(self, value):
        self.context._updateProperty('flash_portal_type_custom', value)

    flash_portal_type_custom = property(get_flash_portal_type_custom, set_flash_portal_type_custom)

    def get_folder_portal_type(self):
        return self.context.folder_portal_type

    def set_folder_portal_type(self, value):
        self.context._updateProperty('folder_portal_type', value)

    folder_portal_type = property(get_folder_portal_type, set_folder_portal_type)

    def get_folder_portal_type_custom(self):
        return self.context.folder_portal_type_custom

    def set_folder_portal_type_custom(self, value):
        self.context._updateProperty('folder_portal_type_custom', value)

    folder_portal_type_custom = property(get_folder_portal_type_custom, set_folder_portal_type_custom)



browserset = FormFieldsets(ICKEditorBrowserSchema)
browserset.id = 'cke_browser'
browserset.label = _(u'CKEditor Browser')

class CKEditorControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(browserset,)

    label = _("CKEditor settings")
    description = _("Control all CKEditor settings for Plone.")
    form_name = _("CKEditor settings")



