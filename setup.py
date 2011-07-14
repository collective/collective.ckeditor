
import os
from setuptools import setup, find_packages

version = '3.6.1dev'

setup(name='collective.ckeditor',
      version=version,
      description="CKEditor for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read() + "\n"
                       + open(os.path.join("docs", "FAQ.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone CKeditor WYSIWYG',
      author='Alterway Solutions',
      author_email='support@ingeniweb.com',
      url='https://svn.plone.org/svn/collective/collective.ckeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.quickupload',
          'collective.plonefinder',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
