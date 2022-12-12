BEWARE
======

The `master` branch of `collective.ckeditor` is now where we are working to support for Plone 5 and Plone 6.

First alpha releases are on their way.

Plone 4 code can be found in `4.x` branch.

TODO before final release
=========================

- fix tests
- fix issues with portal types vocabularies
- upgrade to latest CKEditor 4
- fully remove usage of portal_properties
- integrate work done at TU Dresden

Verify
------

Those notes were taken a while ago with duchenean.
Still need to check what they mean.


 - Continue control panel work to migrate to registry
   - Fix mandatory fields
   - Remove old adapter CKEditorControlPanelAdapter
 - Write a migration from portal properties to portal registry.
 - Remove Flash from quickupload
 - Write upgrade step (P5.1 > P5.2) for css and js bundle


Done
----

- hide profiles that should be hidden in ckeditor
- ckeditor_vars depends on plone
- fix issues with CSS
