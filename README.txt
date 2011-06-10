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
============

when checked out from svn, run utils/base2zope.py at Python prompt.

This will inject the ckeditor directory in a browser Resources directory accessible in line
using this adress::

  - http://yourplonesite/++resource++ckeditor/
  
base2zope.py fix some tal compilation errors (zope.tal bugs), see also::

  - https://bugs.launchpad.net/zope2/+bug/142333
 

More information
================

If you need more support, if you need new plugins for Plone or more generic plugins for ckeditor,
contact us :

- support@ingeniweb.com

