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

then run all editor tests ::

  - open your browser
  
  - http://yourplonesite/++resource++ckeditor/_tests/testall.html

Result,  (0 failed / 361 passedd) 

Install ckeditor
================

  - using portal_quickinstaller


TEST the samples
================

   - http://yourplonesite/++resource++ckeditor/_samples/index.html      


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

collective.plonefinder will be used in future for media browsing and upload 
