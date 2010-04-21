Introduction
============

ckeditor for Plone

Work in progress.

when checked out from svn, run utils/base2zope.py at Python prompt.

This will inject the ckeditor directory in a browser Resources directory accessible in line
using this adress::

  - http://yourplonesite/++resource++ckeditor/
  
base2zope.py fix some tal compilation errors (zope.tal bugs), see also::

  - https://bugs.launchpad.net/zope2/+bug/142333
  
base2zope.py fix also some XHTML errors in ckeditor tests pages.
zope consider html files in browser resources as page templates and return a 404 http error
in case of tal compilation error::

  - http://dev.fckeditor.net/ticket/4416

 

Configure your develop buildout for ckeditor
============================================

This information concerns the svn versions since there's no releases at this time

  - checkout from svn 'collective.ckeditor' https://svn.plone.org/svn/collective/collective.ckeditor/trunk, put it in your develop directory
  - idem for 'collective.plonefinder' https://svn.plone.org/svn/collective/collective.plonefinder/trunk
  - add collective.ckeditor, collective.plonefinder in your develop section  in buildout.cfg
  - add collective.ckeditor to your zcml section
  - add the ckeditor section to run utils/base2zope.py (see buildout/dev.cfg for more information)
  - bin/buildout -c dev.cfg

Install ckeditor in Plone
=========================

  - using portal_quickinstaller


Check the samples
=================

   - http://yourplonesite/++resource++ckeditor/_samples/index.html     


Edit the Plone front-page
=========================

  - It works fine  

Dependencies
============

Plone4 and more.

collective.plonefinder (always in progress at this time) is used for attached media browsing and upload 

get it here https://svn.plone.org/svn/collective/collective.plonefinder/trunk


Plone 3 :
---------

No more support is provided for Plone3.

If you really need ckeditor for Plone contact us support@ingeniweb.com

Otherwise you can always use FCKeditor for Plone.

More information
================

If you need more support, if you need new plugins for Plone or more generic plugins for ckeditor,
contact us :

- support@ingeniweb.com

