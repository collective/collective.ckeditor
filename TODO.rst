BEWARE
======

The `master` branch of `collective.ckeditor` is now where we are working to support for Plone 5 and Plone 6.

First alpha releases are on their way.

Plone 4 code can be found in `4.x` branch.

TODO before final release
=========================

- fix issues with portal types vocabularies
- integrate work done at TU Dresden
- remove references to Flash (do not forget quickupload)

Done
----

- fix warning with @@ckeditor_vars.js (text/plain MIME type)
- hide form.widgets.IRichTextBehavior.text_text_format
- hide profiles that should be hidden in ckeditor
- ckeditor_vars depends on plone
- fix issues with CSS
- Continue control panel work to migrate to registry
  - Fix mandatory fields
  - Remove old adapter CKEditorControlPanelAdapter
- Write a migration from portal properties to portal registry.
- fix tests
- upgrade to latest CKEditor 4
- fully remove usage of portal_properties
