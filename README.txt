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
  - idem for 'iw.resourcetraverser' https://ingeniweb.svn.sourceforge.net/svnroot/ingeniweb/iw.resourcetraverser/trunk
  - add collective.ckeditor, collective.plonefinder and iw.resourcetraverser in your develop section  in buildout.cfg
  - add collective.ckeditor to your zcml section
  - add the ckeditor section to run utils/base2zope.py (see buildout/dev.cfg for more information)
  - bin/buildout -c dev.cfg

Install ckeditor in Plone
=========================

  - using portal_quickinstaller


Check the samples
=================

   - http://yourplonesite/++resource++ckeditor/_samples/index.html     
   

Run ckeditor yui tests
======================
  
  - http://yourplonesite/++resource++ckeditor/_tests/testall.html   
   

Run ckeditor for plone yui tests
================================
  
  - http://yourplonesite/++resource++ckeditor_for_plone/yuitests/ckeditor_plone.html    


Edit the Plone front-page
=========================

  - It works fine  
  
TODO
====

  - Use control panel options in ckeditor_plone.js or ckeditor_ploneconfig.js
  
  - ckeditor control panel improvements :
  
    - easy toolbar selection
    
    - different toolbars upon some options (roles, ...)
    
    - area styles and templates
    
    - other options (spellchecker, copy/paste options, keyboard options)
  
  - plugins integration :
     
    - firefox spellchecker GeckoSpellChecker Plugin
     
    - adapt imgmap plugin for ckeditor
     
    - a new flv player plugin for ckeditor without javascript tags inside html area
     
    - a new flash plugin for ckeditor using swfobject but without javascript tags inside html area
    
  - quick upload without browser (directly from editor insert image dialog box)  

Dependencies
============

iw.resourcetraverser is necessary to permit access to all resources inside 
ckeditor browser directory (otherwise we get some 404 errors), see also :

  -  https://bugs.launchpad.net/bugs/428892

The released version of iw.resourcetraverser can be found here http://products.ingeniweb.com/catalog/iw-resourcetraverser

Thanks to Youenn Boussard

It will be released on pypi in future

collective.plonefinder (always in progress at this time) is used for attached media browsing and upload 

get it here https://svn.plone.org/svn/collective/collective.plonefinder/trunk


More information
================

- support@ingeniweb.com

