#!/usr/bin/env python # -*- coding: UTF-8 -*-
# Authors:
###############################################################################
#                                                                             #
#  This package wraps CKeditor for use in the Zope web application server.    #
#  Copyright (C) 2005 Chad Whitacre < http://www.zetadev.com/ >               #
#                                                                             #
#  This library is free software; you can redistribute it and/or modify it    #
#  under the terms of the GNU Lesser General Public License as published by   #
#  the Free Software Foundation; either version 2.1 of the License, or (at    #
#  your option) any later version.                                            #
#                                                                             #
#  This library is distributed in the hope that it will be useful, but        #
#  WITHOUT ANY WARRANTY; without even the implied warranty of                 #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser    #
#  General Public License for more details.                                   #
#                                                                             #
#  You should have received a copy of the GNU Lesser General Public License   #
#  along with this library; if not, write to the Free Software Foundation,    #
#  Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA                #
#                                                                             #
#                                                                             #
###############################################################################

""" This script takes the CKeditor base distribution in ../src/ and massages it
for use in Zope, outputting to ../browser/ckeditor/. Usage:

    $ ./base2zope.py
    $

"""

from __future__ import print_function
import os
import re
import shutil
import sys
import codecs

from collective import ckeditor
import six
from six.moves import input
ROOT = os.path.dirname(ckeditor.__file__)


def rm_rf(path):
    """ equivalent to rm -rf on Unix
    """
    if os.path.realpath(path) == '/':
        print('will not rm -rf /')  # better safe than sorry :-)
        sys.exit(1)
    else:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def check_dirs(dest_root, src_root):
    """ Decide what to do if source is mùissing or destination is already there
    """

    if not os.path.exists(src_root):
        print("Source directory missing: %s" % src_root)
        exit(2)

    if os.path.exists(dest_root):
        force = sys.argv[1:2] == ['--force']
        if not force:
            answer = input(
                "destination directory already exists; "
                "delete and recreate? (y/n) [n] "
            )
            force = answer.lower() == 'y'
        if force:
            rm_rf(dest_root)
        else:
            sys.exit(1)
    else:
        os.makedirs(dest_root)


ext_unwanted = (
    'asp', 'aspx', 'cfc', 'cfm', 'cgi', 'exe', 'htaccess', 'php',
    'pl', 'lasso', 'afp'
)
# files overloaded
files_unwanted = ()
# files changed
files_changed = {}

# use regexp to fix xhtml errors in tal parser
# (https://bugs.launchpad.net/zope2/+bug/142333)
BADRE = '(?P<start>\/\/\<\!\[CDATA\[[?!\<]*)(?P<tags>.*?)(?P<end>\/\/\]\]\>)'


def makeSkinDirs(srcDir, destDir):
    """
    Now walk the tree and transfer data to our output directory.
    """
    for path, dirs, files in os.walk(srcDir):

        # Determine and maybe create the destination.
        relpath = path[len(srcDir) + 1:]
        destpath = os.path.join(destDir, relpath)
        if not os.path.exists(destpath):
            os.mkdir(destpath)

        for filename in files:

            ext = filename.split('.')[-1]

            src = os.path.join(path, filename)

            dest = os.path.join(destpath, filename)

            # Create the new file if we want it.
            if ext not in ext_unwanted and filename not in files_unwanted:

                if filename in files_changed:

                    # TODO : add Title, description, and image sizes fields
                    # in direct upload forms
                    pass

                # reduce a big frame in WSC Spellchecker (beurk)
                elif filename == 'tmpFrameset.html':
                    inputfile = open(src)
                    outputfile = open(dest, 'w+')
                    for line in inputfile.readlines():
                        if "parseInt( oParams.thirdframeh, 10 )" in line:
                            newline = '    sFramesetRows = "27,*," + \
                            ( parseInt( oParams.thirdframeh, 10 ) || "150" ) +\
                            ",0" ;\r'
                            outputfile.write(newline)
                        else:
                            outputfile.write(line)

                    inputfile.close()
                    outputfile.close()

                else:
                    shutil.copy(src, dest)

                # remove BOM, a known bug on some fckeditor versions
                # (ex: http://sourceforge.net/tracker/index.php?
                # func=detail&aid=1685547&group_id=75348&atid=543653)
                if filename.endswith('.html'):
                    fileObj = codecs.open(dest, "r", "utf-8")
                    u = fileObj.read()
                    fileObj.close()
                    if u.startswith(six.text_type(codecs.BOM_UTF8, "utf8")):
                        fileObj = codecs.open(dest, "w", "utf-8")
                        content = u.lstrip(six.text_type(codecs.BOM_UTF8, "utf8"))
                        fileObj.write(content)
                        fileObj.close()

                # fix xhtml compilation error
                if ext in ('html', 'xml', 'pt'):
                    fileObj = open(dest)
                    content = fileObj.read()
                    fileObj.close()

                    Badtags = re.compile(BADRE, re.IGNORECASE | re.DOTALL)

                    def replace_bad_tags(match):
                        bad = match.group('tags')
                        good = bad.replace('</', '<\/')
                        return match.group('start') + good + match.group('end')

                    content = Badtags.sub(replace_bad_tags, content)

                    # replace empty frame tags by an open frame tag
                    # (another tal compilation error)
                    content = content.replace("></frame>", " />")

                    fileObj = open(dest, "w")
                    fileObj.write(content)
                    fileObj.close()

        # skip svn directories
        if '.svn' in dirs:
            dirs.remove('.svn')


def copy_ckeditor(root):
    SRC_ROOT = os.path.join(root, '_src', 'ckeditor')
    DEST_ROOT = os.path.join(root, 'browser', 'ckeditor')
    check_dirs(DEST_ROOT, SRC_ROOT)
    # Add base skin directory
    makeSkinDirs(SRC_ROOT, DEST_ROOT)
    # TODO :  Add new skins and plugins
    # SRC_SKINS_ADDONS_ROOT = os.path.join(root, '_addons','skins')
    # DEST_SKINS_ADDONS_ROOT = os.path.join(root, 'browser','ckeditor','skins')
    # SRC_PLUGINS_ADDONS_ROOT = os.path.join(root, '_addons','plugins')
    # DEST_PLUGINS_ADDONS_ROOT = os.path.join(root, 'browser','ckeditor',
    #     'plugins')
    # makeSkinDirs(SRC_SKINS_ADDONS_ROOT,DEST_SKINS_ADDONS_ROOT)
    # makeSkinDirs(SRC_PLUGINS_ADDONS_ROOT,DEST_PLUGINS_ADDONS_ROOT)


def tag_entrypoint(data):
    if data['name'] != 'collective.ckeditor':
        return
    root = os.path.join(data['tagdir'], 'src', 'collective', 'ckeditor')
    print("Copying CKEditor code to %s" % root)
    copy_ckeditor(root)


def main():
    PRODUCT_ROOT = os.path.realpath(os.path.join(ROOT))
    copy_ckeditor(PRODUCT_ROOT)


if __name__ == '__main__':
    main()
