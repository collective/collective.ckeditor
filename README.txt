Introduction
============

ckeditor for Plone

Work in progress.

when checked out from svn, run utils/base2zope.py at Python prompt.

This will inject the ckeditor directory in a browser Resources directory accessible in line
using this adress :

  - http://yourplonesite/++resource++ckeditor/
  
base2zope.py fix all tal compilation errors (zope.tal bugs), see also :

  - https://bugs.launchpad.net/zope2/+bug/142333
  
base2zope.py fix also some XHTML errors in ckeditor 
zope consider html files in browser resources as page templates and return a 404 http error
in case of tal compilation error::

  - http://dev.fckeditor.net/ticket/4416

Run all ckeditor yui tests ::
  
  - http://yourplonesite/++resource++ckeditor/_tests/testall.html
 


Install ckeditor
================

  - using portal_quickinstaller


Check the samples
=================

   - http://yourplonesite/++resource++ckeditor/_samples/index.html     
   

Run ckeditor for plone yui tests
================================
  
  - http://yourplonesite/++resource++ckeditor_for_plone/yuitests/ckeditor_plone.html    


Edit the Plone front-page
=========================

  - It works fine  
  
TODO
====

  - Browse and upload medias (collective.plonefinder in progress)
  
  - base config  for Plone
  
  - control panel
  
  - ckeditor MediaWiki plugin integration 
  
  - other old fckeditor plone plugins to make it compliant with ckeditor

Dependencies
============

iw.resourcetraverser is necessary to permit access to all resources inside 
ckeditor browser directory (otherwise we get some 404 errors), see also :

  -  https://bugs.launchpad.net/bugs/428892

iw.resourcetraverser can be found here http://products.ingeniweb.com/catalog/iw-resourcetraverser

Thanks to Youenn Boussard

It will be released on pypi in future

collective.plonefinder (always in progress at this time) is used for attached media browsing and upload 


More information
================

It's a big work to redesign old FCKeditor.Plone features with zope3 and Plone 3.3
technologies and new ckeditor javascript, but it's also a big pleasure, and i can only say one thing :

it will be a blast.

My company (Alter Way / Ingeniweb) support myself of course, but
any kind of external support is really welcome :

- support@ingeniweb.com

