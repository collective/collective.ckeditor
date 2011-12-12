Introduction
============

ckeditor, a wysiwyg editor for Plone 4 and more.

Dependencies
============

Plone4 and more.

collective.plonefinder is used for attached media browsing and upload.

when using buildout or easy_install, collective.plonefinder is installed.

Install collective.ckeditor in your zope instance
=================================================

two options :

- add "collective.ckeditor" in your eggs and zcml sections of your plone 4 buildout
  then run "bin/buildout" or "bin\buildout" under win32
  look at ckeditor.cfg if you are using plone 4 core dev buildout

- >>> easy_install collective.ckeditor

Read docs/INSTALL.txt for more information

Install ckeditor in Plone
=========================

Use the Plone "Add Products" Control Panel.
Choose "CKeditor for Plone 3.x"
Click on Activate
It will also install collective.plonefinder


Plone 3 :
---------

No support is provided for Plone3.

If you really need ckeditor for Plone3 contact us support@ingeniweb.com

You can always use FCKeditor for Plone.


Development
===========

After checking out from svn, run the buildout included in the checkout.

This installs ``copy_ckeditor_code`` script. This script takes care of copying
ckeditor code in the appropriate ``browser/ckeditor`` directory.

The ``browser/ckeditor`` directory makes ckeditor javascript code available to
the browser at::

  http://yourplonesite/++resource++ckeditor/

You need to run ``bin/copy_ckeditor_code`` prior to run ``bin/instance``.
Anyway, if you forget, ``bin/instance`` will break with a
``ConfigurationError``::
  
  Directory .../browser/ckeditor does not exist.
  
Release
=======

Obviously, the ckeditor code also needs to be included in the released eggs.

``collective.ckeditor`` registers an entry point for ``zest.releaser`` that (if
called properly) takes care of copying the code when preparing the release.

However, in order to take advantage of the entry point, you have to use the 
``bin/fullrelease`` locally installed by the development buildout instead of 
a globally installed ``fullrelease``. 

Only the local ``bin/fullrelease`` script can see the entry_point registered by
``collective.ckeditor``. 


More information
================

If you need more support, if you need new plugins for Plone or more generic plugins for ckeditor,
contact us :

- support@ingeniweb.com

