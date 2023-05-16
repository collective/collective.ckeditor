# coding=utf8
import sys
import pytest
import requests
import bs4
from zope_instance import ZopeInstance


@pytest.fixture(scope='module')
def plone_instance(tmp_path_factory, pytestconfig):
    path = tmp_path_factory.mktemp('buildout')
    zi = ZopeInstance(path, pytestconfig)
    zi.run_buildouts()

    with zi:
        yield zi

@pytest.mark.upgrade
def test_plone_is_running(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200

def check_boolean(registry_name, value_to_check):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema." + registry_name,
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value-0")
    assert len(selected) == 1
    checkbox = selected[0]
    assert checkbox.name == "input"
    assert checkbox.attrs.get('type', None) == "checkbox"
    if value_to_check is True:
        assert checkbox.attrs.get('checked', None) == "checked"
    else:
        assert checkbox.attrs.get('checked', None) is None


def check_choice(registry_name, value_to_check):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema." + registry_name,
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("option[selected]")
    assert len(selected) == 1
    option = selected[0]
    assert value_to_check in str(option)


def check_list(registry_name, upgraded_lines, default_lines=None):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema." + registry_name,
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    textarea = selected[0]
    assert textarea.name == "textarea"
    for line in upgraded_lines.splitlines():
        assert line.strip() in textarea.text
    if default_lines:
        for line in default_lines.splitlines():
            if line.strip():
                assert line.strip() not in textarea.text


@pytest.mark.upgrade
def test_deletion_of_ckeditor_properties(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_properties/manage_main",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    assert "ckeditor_properties" not in request.text


@pytest.mark.upgrade
def test_upgrade_of_forcePasteAsPlainText(plone_instance):
    check_boolean('forcePasteAsPlainText', True)


@pytest.mark.upgrade
def test_upgrade_of_skin(plone_instance):
    check_choice('skin', 'Flat buttons')


@pytest.mark.upgrade
def test_upgrade_of_toolbar(plone_instance):
    check_choice('toolbar', 'Custom Toolbar')


@pytest.mark.upgrade
def test_upgrade_of_toolbar_Custom(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.toolbar_Custom",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    textarea = selected[0]
    assert textarea.name == "textarea"
    toolbar_Custom = """
[
['Cut','-','AjaxSave'],
['TextColor','ShowBlocks'],
]
"""
    for line in toolbar_Custom.splitlines():
        assert line.strip() in textarea.text


@pytest.mark.upgrade
def test_upgrade_of_filtering(plone_instance):
    check_choice('filtering', 'Disabled')


@pytest.mark.upgrade
def test_upgrade_of_customAllowedContent(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.customAllowedContent",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    textarea = selected[0]
    assert textarea.name == "textarea"
    customAllowedContent = """
['p h2']
"""
    for line in customAllowedContent.splitlines():
        assert line.strip() in textarea.text


@pytest.mark.upgrade
def test_upgrade_of_extraAllowedContent(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.extraAllowedContent",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    textarea = selected[0]
    assert textarea.name == "textarea"
    extraAllowedContent = """
['h3']
"""
    for line in extraAllowedContent.splitlines():
        assert line.strip() in textarea.text


@pytest.mark.upgrade
def test_upgrade_of_disallowedContent(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.disallowedContent",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    textarea = selected[0]
    assert textarea.name == "textarea"
    disallowedContent = """
'h1'
"""
    for line in disallowedContent.splitlines():
        assert line.strip() in textarea.text


@pytest.mark.upgrade
def test_upgrade_of_menuStyles(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.menuStyles",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    field = selected[0]
    assert field.name == "textarea"
    menuStyle = """
    { name : 'upgrade ascii Title'		, element : 'h2', styles : { 'color' : '#888' } },
    { name : 'upgrade unicode Title éè'		, element : 'h2', styles : { 'color' : '#888' } },
    """
    IS_PYTHON2 = sys.version_info[0] == 2
    if IS_PYTHON2:
        menuStyle = menuStyle.decode('utf8')
    for line in menuStyle.splitlines():
        assert line.strip() in field.text


@pytest.mark.upgrade
def test_upgrade_of_plugins(plone_instance):
    upgradedValues = """
    ajaxsave;/++resource++cke_ajaxsave/plugin.js
    """
    defaultValues = """
    uploadwidget;/++resource++ckeditor/plugins/uploadwidget/plugin.js
    uploadimage;/++resource++ckeditor/plugins/uploadimage/plugin.js
    """
    check_list('plugins', upgradedValues, defaultValues)


@pytest.mark.upgrade
def test_upgrade_of_removePlugins(plone_instance):
    upgradedValues = """image"""
    check_list('removePlugins', upgradedValues)


@pytest.mark.upgrade
def test_upgrade_of_customTemplates(plone_instance):
    customTemplates = """
    ++resource++upgrade_javascripts/upgrade_templates.js
    """
    check_list('customTemplates', customTemplates)


@pytest.mark.upgrade
def test_upgrade_of_templatesReplaceContent(plone_instance):
    check_boolean('templatesReplaceContent', True)


@pytest.mark.upgrade
def test_upgrade_of_enableScaytOnStartup(plone_instance):
    check_boolean('enableScaytOnStartup', True)


@pytest.mark.upgrade
def test_upgrade_of_bodyId(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.bodyId",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    field = selected[0]
    assert field.name == "input"
    assert field.get('type', None) == "text"
    assert field.get('value', None) == "upgrade"


@pytest.mark.upgrade
def test_upgrade_of_bodyClass(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.bodyClass",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    field = selected[0]
    assert field.name == "input"
    assert field.get('type', None) == "text"
    assert field.get('value', None) == "upgrade"


@pytest.mark.upgrade
def test_upgrade_of_defaultTableWidth(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.defaultTableWidth",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    input_field = selected[0]
    assert input_field.name == "input"

    defaultTableWidth = "250px"
    assert defaultTableWidth == input_field["value"]


@pytest.mark.upgrade
def test_upgrade_of_width(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.width",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    input_field = selected[0]
    assert input_field.name == "input"

    width = "200"
    assert width == input_field["value"]


@pytest.mark.upgrade
def test_upgrade_of_height(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.height",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    input_field = selected[0]
    assert input_field.name == "input"

    height = "200"
    assert height == input_field["value"]


@pytest.mark.upgrade
def test_upgrade_of_allow_link_byuid(plone_instance):
    check_boolean('allow_link_byuid', False)


@pytest.mark.upgrade
def test_upgrade_of_allow_relative_links(plone_instance):
    check_boolean('allow_relative_links', False)


@pytest.mark.upgrade
def test_upgrade_of_allow_server_browsing(plone_instance):
    check_boolean('allow_server_browsing', False)


@pytest.mark.upgrade
def test_upgrade_of_allow_file_upload(plone_instance):
    check_boolean('allow_file_upload', False)


@pytest.mark.upgrade
def test_upgrade_of_allow_image_upload(plone_instance):
    check_boolean('allow_image_upload', False)


@pytest.mark.upgrade
def test_upgrade_of_allow_flash_upload(plone_instance):
    check_boolean('allow_flash_upload', False)


@pytest.mark.upgrade
def test_upgrade_of_allow_folder_creation(plone_instance):
    check_boolean('allow_folder_creation', False)


@pytest.mark.upgrade
def test_upgrade_of_file_portal_type(plone_instance):
    check_choice('file_portal_type', 'custom')


@pytest.mark.upgrade
def test_upgrade_of_file_portal_type_custom(plone_instance):
    upgradedValues = """
    *|MyFile
    Folder|MyFile
"""
    defaultValues = """
    *|File
    Folder|File
"""
    check_list('file_portal_type_custom', upgradedValues, defaultValues)


@pytest.mark.upgrade
def test_upgrade_of_image_portal_type(plone_instance):
    check_choice('image_portal_type', 'custom')


@pytest.mark.upgrade
def test_upgrade_of_image_portal_type_custom(plone_instance):
    upgradedValues = """
    *|MyImage
    Folder|MyImage
"""
    defaultValues = """
    *|Image
    Folder|Image
"""
    check_list('image_portal_type_custom', upgradedValues, defaultValues)


@pytest.mark.upgrade
def test_upgrade_of_browse_images_portal_types(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.browse_images_portal_types",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value-to")
    assert len(selected) == 1
    select_to = selected[0]
    assert select_to.name == "select"
    assert "News Item (portal type: News Item, product:" in select_to.text
    selected = soup.select("#form-widgets-value-from")
    assert len(selected) == 1
    select_from = selected[0]
    assert select_from.name == "select"
    assert "Image (portal type: Image, product:" in select_from.text


@pytest.mark.upgrade
def test_upgrade_of_flash_portal_type(plone_instance):
    check_choice('flash_portal_type', 'custom')


@pytest.mark.upgrade
def test_upgrade_of_flash_portal_type_custom(plone_instance):
    upgradedValues = """
    *|MyFile
    Folder|MyFile
"""
    defaultValues = """
    *|File
    Folder|File
"""
    check_list('flash_portal_type_custom', upgradedValues, defaultValues)


@pytest.mark.upgrade
def test_upgrade_of_browse_flashs_portal_types(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.browse_flashs_portal_types",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value-to")
    assert len(selected) == 1
    select = selected[0]
    assert select.name == "select"
    assert "File (portal type: File, product:" in select.text
    selected = soup.select("#form-widgets-value-from option")
    assert len(selected) == 0


@pytest.mark.upgrade
def test_upgrade_of_folder_portal_type(plone_instance):
    check_choice('folder_portal_type', 'custom')


@pytest.mark.upgrade
def test_upgrade_of_folder_portal_type_custom(plone_instance):
    upgradedValues = """
    *|MyFolder
"""
    defaultValues = """
    *|Folder
"""
    check_list('folder_portal_type_custom', upgradedValues, defaultValues)


@pytest.mark.upgrade
def test_upgrade_of_properties_overloaded(plone_instance):
    upgradedValues = """
    height
    """
    defaultValues = """
    width
    """
    check_list('overloadable_properties', upgradedValues, defaultValues)


@pytest.mark.upgrade
def test_upgrade_of_entities(plone_instance):
    check_boolean('entities', True)


@pytest.mark.upgrade
def test_upgrade_of_entities_greek(plone_instance):
    check_boolean('entities_greek', True)


@pytest.mark.upgrade
def test_upgrade_of_entities_latin(plone_instance):
    check_boolean('entities_latin', True)


@pytest.mark.upgrade
def test_upgrade_of_image2_captionedClass(plone_instance):
    request = requests.get(
        "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.image2_captionedClass",
        auth=("admin", "admin"),
    )
    assert request.status_code == 200
    soup = bs4.BeautifulSoup(request.text)
    selected = soup.select("#form-widgets-value")
    assert len(selected) == 1
    field = selected[0]
    assert field.name == "input"
    assert field.get('type', None) == "text"
    assert field.get('value', None) == "my_image"


@pytest.mark.upgrade
def test_upgrade_of_image2_alignClasses(plone_instance):
    upgradedValues = """
    myimageleft
    myimagedummy
    myimageright
    """
    defaultValues = """
    image-left
    image-dummy
    image-right
    """
    check_list('image2_alignClasses', upgradedValues, defaultValues)
