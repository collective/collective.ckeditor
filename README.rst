Introduction
============

ckeditor, a wysiwyg editor for Plone 4 and more.

How to install
==============

You can install it as any Plone addon. Please follow official documentation_.

No support is provided for Plone3.
If you really need ckeditor for Plone3 contact us support@ingeniweb.com
You can always use FCKeditor_ for Plone.

Dependencies
------------

* Plone >= 4
* collective.plonefinder_

Development
-----------

After checking out sources, run the included buildout.

This installs ``copy_ckeditor_code`` script. This script takes care of copying
ckeditor code in the appropriate ``browser/ckeditor`` directory.

The ``browser/ckeditor`` directory makes ckeditor javascript code available to
the browser at::

  http://yourplonesite/++resource++ckeditor/

You need to run ``bin/copy_ckeditor_code`` prior to run any Zope/Plone instance
with your development ``collective.ckeditor``.
Anyway, if you forget, your instance will break with a ``ConfigurationError``::
  
  Directory .../browser/ckeditor does not exist.
  
How to Release
--------------

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

If you need more support, if you need new plugins for Plone or more generic
plugins for ckeditor, please contact us at support@ingeniweb.com

Credits
=======

Companies
---------

Ingéniweb

- `Contact us <mailto:support@ingeniweb.com>`_

Contributors
------------

- Kai Lautaportti <kai.lautaportti@hexagonit.fi>
- Giacomo Spettoli <giacomo.spettoli@gmail.com>
- Godefroid Chapelle <gotcha@bubblenet.be>
- Mathieu Le Marec - Pasquet <kiorky@cryptelium.net>
- Jean-Mat Grimaldi <jeanmat.grimaldi@gmail.com>
- Michael Smith <msmith64@naz.edu>
- Victor Fernandez de Alba <sneridagh@gmail.com>
- Kim Paulissen <spereverde@gmail.com>
- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
.. _FCKEditor: http://plone.org/fckeditor
