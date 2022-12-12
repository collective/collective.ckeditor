import os
import sys
from setuptools import setup, find_packages

version = '5.0.0a2'

long_description = (
    open("TODO.rst").read() + "\n"
    + open("README.rst").read() + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read() + "\n"
    + open(os.path.join("docs", "FAQ.txt")).read()
)

install_requires = [
    'setuptools',
    'zope.i18nmessageid',
    'collective.quickupload',
    'collective.plonefinder',
    'plone.app.uuid',
    'plone.api',
]

if sys.version_info[0] < 3:
    install_requires.append('demjson')
else:
    install_requires.append('demjson3')

setup(
    name='collective.ckeditor',
    version=version,
    description="CKEditor for Plone",
    long_description=long_description,
    python_requires=
        '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*,',
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='Plone CKeditor WYSIWYG',
    author='Plone Collective (started by Alterway Solutions)',
    author_email='toutpt@gmail.com',
    url='https://github.com/collective/collective.ckeditor',
    license='GPL',
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require=dict(
        test=[
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
        pytest=[
            "pytest",
            "gocept.pytestlayer",
            "pathlib2",
            "requests",
        ],
    ),
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
