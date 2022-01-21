import pytest
import requests
from zope_instance import ZopeInstance


@pytest.fixture
def plone_instance(tmp_path, pytestconfig):
    return ZopeInstance(tmp_path, pytestconfig)


@pytest.mark.upgrade
def test(plone_instance):
    plone_instance.run_buildouts("collective.ckeditor=4.10.1")
    with plone_instance:
        r = requests.get(
            "http://localhost:8080/Plone/portal_properties/manage_main",
            auth=("admin", "admin"),
        )
        assert r.status_code == 200
        assert "ckeditor_properties" not in r.text

        r = requests.get(
            "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.forcePasteAsPlainText",
            auth=("admin", "admin"),
        )
        assert r.status_code == 200
        assert (
            """<input type="checkbox" id="form-widgets-value-0" name="form.widgets.value:list" class="single-checkbox-widget bool-field" value="selected" checked="checked" />"""
            in r.text
        )

        r = requests.get(
            "http://localhost:8080/Plone/portal_registry/edit/collective.ckeditor.browser.ckeditorsettings.ICKEditorSchema.skin",
            auth=("admin", "admin"),
        )
        assert r.status_code == 200
        assert "moono-lisa" in r.text
