import os
from setuptools import setup, find_packages

version = '4.10.1'

long_description = (
    open("README.rst").read() + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read() + "\n"
    + open(os.path.join("docs", "FAQ.txt")).read()
)

setup(
    name='collective.ckeditor',
    version=version,
    description="CKEditor for Plone",
    long_description=long_description,
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
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Plone CKeditor WYSIWYG',
    author='Alterway Solutions',
    author_email='toutpt@gmail.com',
    url='https://github.com/collective/collective.ckeditor',
    license='GPL',
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.i18nmessageid',
        'collective.quickupload',
        'collective.plonefinder',
        'plone.app.uuid',
        'demjson',
        'plone.api',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
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
