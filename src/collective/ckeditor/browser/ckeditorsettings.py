from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from zope.interface import implementer, Interface
from zope.component import adapter
try:
    from zope.component.hooks import getSite
except:  # Plone < 4.3
    from zope.app.component.hooks import getSite

from zope.schema import Bool
from zope.schema import Text
from zope.schema import TextLine
from zope.schema import Choice
from zope.schema import Tuple
from zope.schema import List

from z3c.form import field
from z3c.form import group

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

# from plone.fieldsets.fieldsets import FormFieldsets

from collective.ckeditor import siteMessageFactory as _


class ICKEditorBaseSchema(Interface):
    """
    CKEditor Base fieldset schema
    """

    skin = Choice(
        title=_(u"Skin"),
        description=_(u"Choose the editor skin."),
        required=True,
        default='moonocolor',
        vocabulary="collective.ckeditor.vocabularies.skin")

    forcePasteAsPlainText = Bool(
        title=_(u"Force paste as plain text"),
        description=_(u"Choose if you want to remove format on copy/paste, "
                      "and paste only text and CR/LF"),
        default=False,
        required=False)

    toolbar = Choice(
        title=_(u"Toolbar"),
        description=_(u"Choose the editor toolbar, "
                      "edit the next field if you choose a Custom toolbar'."),
        required=True,
        default='Plone',
        vocabulary="collective.ckeditor.vocabularies.toolbar")

    toolbar_Custom = Text(
        title=_(u"Customized Toolbar"),
        description=_(u"Build your own CKEditor Toolbar. "
                      "Take care with the javascript syntax. "
                      "If you want to add new plugins, "
                      "add new buttons here if needed."),
        required=False)

    filtering = Choice(
        title=_(u"Filtering"),
        description=_(
            u"Setup of Advanced Content Filter. "
            u"Read documentation at "
            u"http://docs.ckeditor.com/#!/guide/dev_advanced_content_filter"
        ),
        required=True,
        default='default',
        vocabulary="collective.ckeditor.vocabularies.filtering")

    customAllowedContent = Text(
        title=_(u"Custom Allowed Content"),
        description=_(
            u"Configuration of custom filtering. "
            u"Taken in account only if Filtering option is 'Custom'. "
            u"Use Javascript syntax. Read documentation at "
            u"http://docs.ckeditor.com/#!/guide/dev_allowed_content_rules"
        ),
        required=False)

    extraAllowedContent = Text(
        title=_(u"Extra Allowed Content"),
        description=_(
            u"Extra rules on top of automatic filtering. "
            u"Taken in account only if Filtering option is 'Automatic'. "
            u"Use Javascript syntax. Read documentation at "
            u"http://docs.ckeditor.com/#!/guide/dev_allowed_content_rules"
        ),
        required=False)

    disallowedContent = Text(
        title=_(u"Disallowed Content"),
        description=_(
            u"The Disallowed Content feature complements the Allowed "
            u"Content feature in that it lets you explicitly blacklist "
            u"elements that you do not want to have in your CKEditor content. "
            u"Taken in account only if Filtering option is not set to 'Disabled'. "
            u"Use Javascript syntax. Read documentation at "
            u"http://docs.ckeditor.com/#!/guide/dev_disallowed_content"
        ),
        required=False)

    menuStyles = Text(
        title=_(u"Menu styles"),
        description=_(u"Build your own CKEditor menu styles Combo box. "
                      u"Take care with the javascript syntax. "
                      u"If you want to use css classes or ids, "
                      u"the attributes must exist in your css."),
        required=False)

    bodyId = TextLine(
        title=_(u"Area Body Id"),
        description=_(u"Enter the css id applied to the "
                      "body tag of the editor area"),
        default=u'content',
        required=False)

    plugins = List(
        title=_(u"Plugins"),
        description=_(u"Plugin format is 'id;relative path'."),
        value_type=TextLine(),
        required=False)

    removePlugins = List(
        title=_(u"Plugins to remove"),
        description=_(u"List of plugins to remove, one plugin per line. Plugin format is 'id'."),
        value_type=TextLine(),
        required=False)

    bodyClass = TextLine(
        title=_(u"Area Body Class"),
        description=_(u"Enter the css class name applied to the "
                      "body tag of the editor area"),
        required=False)

    customTemplates = List(
        title=_(u"Custom templates"),
        description=_(u"URLs of Javascript "
                      "files that register custom templates"),
        value_type=TextLine(),
        required=False)

    templatesReplaceContent = Bool(
        title=_(u"Templates will replace the current contents "
                "of the visual editor window"),
        description=_(u"Choose if you want templates to replace "
                      "the contents when inserted"),
        default=False,
        required=False)

    enableScaytOnStartup = Bool(
        title=_(u"Enable SCAYT on startup"),
        description=_(u"Choose if you want SCAYT to be automatically "
                      "enabled while the editor is loaded.  This will only "
                      "be the case if a relevant language can be used "
                      "in SCAYT availble ones."),
        default=False,
        required=False)

    defaultTableWidth = TextLine(
        title=_(u"Default Table Width"),
        description=_(u"Enter the default table width"),
        default=u"500px",
        required=False)


class ICKEditorSkinSchema(Interface):
    """
    CKEditor Skin fieldset schema
    """
    width = TextLine(
        title=_(u"Editor width"),
        description=_(u"Enter the width of the editor in px % or em"),
        required=False)

    height = TextLine(
        title=_(u"Editor height"),
        description=_(u"Enter the height of the editor in px % or em"),
        required=False)


class ICKEditorBrowserSchema(Interface):
    """
    CKEditor Browser fieldset schema
    """
    allow_link_byuid = Bool(
        title=_(u"Allow link objects by UID"),
        description=_(u"Check if you want url with Unique ID "
                      "(no more 404 errors when moving objects). "
                      "Notice that portal_transforms in standard "
                      "configuration transforms uid links in absolute urls "
                      "in view displays."),
        default=True,
        required=False)

    allow_relative_links = Bool(
        title=_(u"Allow relative urls transformation"),
        description=_(u"Check if you want relative urls after saving forms. "
                      "Useful when link by uid is not checked."),
        default=False,
        required=False)

    allow_server_browsing = Bool(
        title=_(u"Allow browsing for links"),
        description=_(u"Check to allow server browsing"
                      "used for medias linking."),
        default=True,
        required=False)

    allow_file_upload = Bool(
        title=_(u"Allow file upload"),
        description=_(u"Check to allow files upload in link dialog boxes)."),
        default=False,
        required=False)

    allow_image_upload = Bool(
        title=_(u"Allow image upload"),
        description=_(u"Check to allow upload for images."),
        default=False,
        required=False)

    allow_flash_upload = Bool(
        title=_(u"Allow flash upload"),
        description=_(u"Check to allow upload for flash content."),
        default=False,
        required=False)

    allow_folder_creation = Bool(
        title=_(u"Allow folder creation"),
        description=_(u"Check to allow folder creation in browser."),
        default=False,
        required=False)

    file_portal_type = Choice(
        title=_(u"File portal type"),
        description=_(u"Choose the portal type used for file upload."),
        required=True,
        default='File',
        vocabulary="collective.ckeditor.vocabularies.FileTypeUpload")

    file_portal_type_custom = List(
        title=_(u"Custom File portal type for upload"),
        description=_(u"Add list of pairs CONTAINER_TYPE|FILE_TYPE. "
                      "The file portal type choosen for upload will depend "
                      "on contextual container portal type. "
                      "* means any portal type."
                      "Take care, no control is done over this field value."),
        required=False,
        value_type=TextLine(),
        default=['*|File', 'Folder|File', ])

    browse_images_portal_types = Tuple(
        title=_(u"Portal Types for images linking"),
        description=_(u"Choose the types used "
                      "for images selection in browser."),
        required=True,
        missing_value=tuple(),
        default=('Image', 'News Item',),
        value_type=Choice(
            vocabulary="collective.ckeditor.vocabularies.ImageTypes"))

    image_portal_type = Choice(
        title=_(u"Image portal type"),
        description=_(u"Choose the portal type used for image upload."),
        required=True,
        default='auto',
        vocabulary="collective.ckeditor.vocabularies.ImageTypeUpload")

    image_portal_type_custom = List(
        title=_(u"Custom Image portal type for upload"),
        description=_(u"Add list of pairs CONTAINER_TYPE|IMAGE_TYPE. "
                      "The image portal type choosen for upload will depend "
                      "on contextual container portal type. "
                      "* means any portal type."
                      "Take care, no control is done over this field value."),
        required=False,
        value_type=TextLine(),
        default=['*|Image', 'Folder|Image', ])

    browse_flashs_portal_types = Tuple(
        title=_(u"Portal Types for flash contents linking"),
        description=_(u"Choose the types used "
                      "for flash contents selection in browser."),
        required=True,
        missing_value=tuple(),
        default=('File',),
        value_type=Choice(
            vocabulary="collective.ckeditor.vocabularies.FileTypes"))

    flash_portal_type = Choice(
        title=_(u"Flash portal type"),
        description=_(u"Choose the portal type used for flash content upload"),
        required=True,
        default='File',
        vocabulary="collective.ckeditor.vocabularies.FileTypeUpload")

    flash_portal_type_custom = List(
        title=_(u"Custom Flash portal type for upload"),
        description=_(u"Add list of pairs CONTAINER_TYPE|FLASH_TYPE. "
                      "The flash portal type choosen for upload will depend "
                      "on contextual container portal type. "
                      "* means any portal type. "
                      "Take care, no control is done over this field value."),
        required=False,
        value_type=TextLine(),
        default=['*|File', 'Folder|File', ])

    folder_portal_type = Choice(
        title=_(u"Folder portal type"),
        description=_(u"Choose the portal type used for folder creation"),
        required=True,
        default='Folder',
        vocabulary="collective.ckeditor.vocabularies.FolderTypes")

    folder_portal_type_custom = List(
        title=_(u"Custom portal type for folder creation"),
        description=_(u"Add list of pairs CONTAINER_TYPE|FOLDER_TYPE. "
                      "The folder portal type choosen for folders creation "
                      "will depend on contextual container portal type. "
                      "* means any portal type. "
                      "Take care, no control is done over this field value."),
        required=False,
        value_type=TextLine(),
        default=['*|Folder', 'Large Plone Folder|Large Plone Folder', ])


class ICKEditorAdvancedSchema(Interface):
    """
    CKEditor Advanced schema
    """
    overloadable_properties = List(
        title=_(u"Widget overload"),
        description=_(u"If you want some cke control panel properties "
                      "overload local field widget properties, enter the "
                      "properties names list here. "
                      "Example, enter 'width' and 'height' to get always "
                      "the same values. Look at "
                      "ZMI > portal_properties > ckeditor_properties "
                      "for all properties names."),
        required=False,
        value_type=TextLine(),
        default=['width', ],)

    entities = Bool(
        title=_(u"Html Entities"),
        description=_(u"Whether to use Html entities in the editor."),
        default=False,
        required=False)

    entities_greek = Bool(
        title=_(u"Greek Html Entities"),
        description=_(u"Whether to convert some symbols, mathematical "
                      "symbols, and Greek letters to Html entities."),
        default=False,
        required=False)

    entities_latin = Bool(
        title=_(u"Latin Html Entities"),
        description=_(u"Whether to convert some Latin characters "
                      "Latin alphabet No. 1, ISO 8859-1) to Html entities."),
        default=False,
        required=False)

    image2_captionedClass = Text(
        title=_(u"Captioned image class (image2)"),
        description=_(u"CSS class applied by image2 plugin to"
                      "the <figure> element of a captioned image."),
        default=u"image",
        required=False)

    image2_alignClasses = List(
        title=_(u"Align classes (image2)"),
        description=_(u"3 CSS classes applied by image2 plugin to"
                      "specify alignment (left, center, right)."),
        required=False,
        value_type=TextLine(),
        default=[],)


class ICKEditorSchema(ICKEditorBaseSchema, ICKEditorSkinSchema,
                      ICKEditorBrowserSchema, ICKEditorAdvancedSchema):
    """Combined schema for the adapter lookup.
    """


class CKEditorBaseSchemaForm(group.GroupForm):
    label = _(u"Basic settings")
    fields = field.Fields(ICKEditorBaseSchema)


class CKEditorSkinSchemaForm(group.GroupForm):
    label = _(u"Editor Skin")
    fields = field.Fields(ICKEditorSkinSchema)


class CKEditorBrowserSchemaForm(group.GroupForm):
    label = _(u"Resources Browser")
    fields = field.Fields(ICKEditorBrowserSchema)


class CKEditorAdvancedSchemaForm(group.GroupForm):
    label = _(u"Advanced Configuration")
    fields = field.Fields(ICKEditorAdvancedSchema)


class CKEditorControlPanelForm(RegistryEditForm):
    schema = ICKEditorSchema
    # form_fields = FormFieldsets(basicset, skinset, browserset, advancedset)
    label = _("CKEditor settings")
    description = _("Control CKEditor settings for Plone.")
    form_name = _("CKEditor settings")
    groups = (CKEditorBaseSchemaForm, CKEditorSkinSchemaForm, CKEditorBrowserSchemaForm, CKEditorAdvancedSchemaForm)


class CKEditorControlPanel(ControlPanelFormWrapper):
    form = CKEditorControlPanelForm
