
import os
from setuptools import setup, find_packages

version = '3.6.7'

setup(name='collective.ckeditor',
      version=version,
      description="CKEditor for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read() + "\n"
                       + open(os.path.join("docs", "FAQ.txt")).read(),
      classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        ],
      keywords='Plone CKeditor WYSIWYG',
      author='Alterway Solutions',
      author_email='toutpt@gmail.com',
      url='https://github.com/collective/collective.ckeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.i18nmessageid',
          'collective.quickupload',
          'collective.plonefinder',
          'demjson',
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
               'copy_ckeditor_code = collective.ckeditor.utils.base2zope:main',
        ],
        'zest.releaser.releaser.after_checkout': [
            'prepare = collective.ckeditor.utils.base2zope:tag_entrypoint',
        ],
        'z3c.autoinclude.plugin': [
            'target = plone',
        ],
      },
      )
