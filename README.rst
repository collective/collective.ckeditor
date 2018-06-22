.. image:: https://travis-ci.org/collective/collective.ckeditor.svg
    :target: https://travis-ci.org/collective/collective.ckeditor
.. image:: https://coveralls.io/repos/collective/collective.ckeditor/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/collective/collective.ckeditor?branch=master


Introduction
============

This addon is a ckeditor_ integration for Plone.  This release includes ckeditor_ version 4.9.2.

.. contents::

How to install
==============

You can install it as any Plone addon. Please follow official documentation_.

The code source can be found at
https://github.com/collective/collective.ckeditor

Please report issues at
https://github.com/collective/collective.ckeditor/issues

Dependencies
------------

* Plone >= 4
* collective.plonefinder_

Upgrades
========

Go to ZMI-->portal_setup-->Upgrades, choose "collective.ckeditor:default"
profile and execute the upgrade steps.

4.3.0
-----

Release 4.3.0 comes with the **Enhanced Image** plugin (`image2`). It is not
enabled by default as it removes some of the advanced functionality provided by
the default image plugin (`image`). However, the **Enhanced Image** plugin
provides the ability to add a caption together with the image. It is also much
more user-friendly.

To enable the plugin, you need to setup `ckeditor_properties` through generic
setup `propertiestool.xml`::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
   <object name="ckeditor_properties" meta_type="Plone Property Sheet">
    <property name="removePlugins" type="lines">
     <element value="image"/>
    </property>
    <property name="plugins" type="lines">
     <element value="ajaxsave;/++resource++cke_ajaxsave/plugin.js"/>
     <element value="image2;/++resource++ckeditor/plugins/image2/plugin.js"/>
    </property>
   </object>
  </object>

This disables the `image` (default) plugin and enables the `image2` plugin.

The `image2` plugin comes with two specific settings (configurable only through
generic setup)::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
   <object name="ckeditor_properties" meta_type="Plone Property Sheet">
    <property name="image2_captionedClass" type="string">image</property>
    <property name="image2_alignClasses" type="lines">
     <element value="image-left"/>
     <element value="image-dummy"/>
     <element value="image-right"/>
    </property>
   </object>
  </object>

The settings are `image2_captionedClass` and `image2_alignClasses`.
The values above are the default values.

If you enable the plugin, you also need to setup Plone to accept 
the `figcaption` tag.

This is done by configuring HTML filtering with a setup handler like::

  def enable_figcaption(p):
      """ Allow figcaption as valid tag in portal_transforms safe_html"""

      from Products.PortalTransforms.Transform import make_config_persistent

      pt = getToolByName(p, 'portal_transforms')
      tid = 'safe_html'
      if not tid in pt.objectIds():
          return
      trans = pt[tid]
      tconfig = trans._config

      validtags = tconfig['valid_tags']
      validtags.update({'figcaption': 1})

      make_config_persistent(tconfig)
      trans._p_changed = True
      trans.reload()
      log.info('added figcaption as valid tag')

CKEditor plugins
================

`balloontoolbar` plugin
-----------------------
provided since version 4.8.0

Not enabled by default, this plugin provides an API to setup context sensitive toolbars.

To enable the plugin, add ``balloontoolbar;/++resource++ckeditor/plugins/balloontoolbar/plugin.js``
to the `Plugins` field in CKEditor control panel (``@@ckeditor-controlpanel``).

`uploadimage` plugin
--------------------
provided since version 4.7.0

Enabled by default, this plugin manages support for uploading images that were dropped or pasted into the editor.

`nonbreaking` plugin
--------------------
provided since version 4.4.5.

When enabled, the plugin provides keyboard shortcuts to insert non breaking chars:

- ``Ctrl-Alt-Space`` for non breaking space,
- ``Ctrl-Alt-Hyphen`` for non breaking hyphen.

Corresponding buttons can also be configured in the toolbar:

- ``NbSpace``
- ``NbHyphen``

To enable the plugin, add ``nonbreaking;/++resource++cke_nonbreaking/plugin.js``
to the `Plugins` field in CKEditor control panel (``@@ckeditor-controlpanel``).

Or setup `ckeditor_properties` through generic setup `propertiestool.xml`::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
   <object name="ckeditor_properties" meta_type="Plone Property Sheet">
    <property name="plugins" type="lines">
     <element value="ajaxsave;/++resource++cke_ajaxsave/plugin.js"/>
     <element value="nonbreaking;/++resource++cke_nonbreaking/plugin.js"/>
    </property>
   </object>
  </object>

`tableresize` plugin
--------------------

When enabled, the plugin makes it easy to change the table columns width by
drag/dropping it from left to right and right to left.

To enable the plugin, add ``tableresize;/++resource++ckeditor/plugins/tableresize/plugin.js``
to the `Plugins` field in CKEditor control panel (``@@ckeditor-controlpanel``).

Or setup `ckeditor_properties` through generic setup `propertiestool.xml`::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
   <object name="ckeditor_properties" meta_type="Plone Property Sheet">
    <property name="plugins" type="lines" purge="False">
     <element value="tableresize;/++resource++ckeditor/plugins/tableresize/plugin.js"/>
    </property>
   </object>
  </object>

Development
===========

.. attention:: 
    ConfigurationError 

    If you try to run a Zope/Plone instance with a collective.ckeditor
    checkout, your instance will break with a ``ConfigurationError``::

      Directory .../browser/ckeditor does not exist.

After checking out collective.ckeditor sources, run the included buildout.

This installs and runs the ``copy_ckeditor_code`` script.  It takes care of
copying ckeditor code in the appropriate ``browser/ckeditor`` directory.

The ``browser/ckeditor`` directory makes ckeditor javascript code available to
the browser at::

  http://yourplonesite/++resource++ckeditor/

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

How to update to a newer version of CKEditor
--------------------------------------------

Valid for CKEditor 4

1. Go to ``dev/build-ckeditor``
2. Update plugin versions computation in ``image2.sh``, ``moono.sh``,
   ``scayt`` and ``wsc`` in ``scayt.sh``
3. Issue the following command ``CKEDITOR_VERSION=4.x.x make``
4. Run ``bin/copy_ckeditor_code``
5. Test
6. Add untracked files ``git add ../../src/collective/ckeditor/_src/ckeditor/``
7. Commit

If you need unminified JS to debug the release,
step 3 can be replaced with::

  MINIFIED_JS=--leave-js-unminified CKEDITOR_VERSION=4.x.x make

Tests status
------------

.. image:: https://secure.travis-ci.org/collective/collective.ckeditor.png
    :target: http://travis-ci.org/collective/collective.ckeditor

Credits
=======

Companies
---------

* `Makina Corpus <http://www.makina-corpus.com>`_
* `Ecreall <http://www.ecreall.com>`_
* `BubbleNet <http://bubblenet.be>`_
* `Hexagonit <http://www.hexagonit.fi>`_

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
- Jean-Michel FRANCOIS aka toutpt <toutpt@gmail.com>
- Gauthier Bastien <gauthier@imio.be>

.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
.. _FCKEditor: http://plone.org/fckeditor
.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _ckeditor: http://ckeditor.com/
.. _collective.plonefinder: http://plone.org/products/collective.plonefinder
