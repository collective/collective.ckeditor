import os
import sys
import time
import subprocess
import pathlib2 as pathlib
import socket
from contextlib import closing


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


class ZopeInstance(object):
    def __init__(
        self,
        tmp_path,
        pytestconfig,
        host="127.0.0.1",
        port=8080,
    ):
        self.host = host
        self.port = port
        self.check_port()
        buildout_exe = pathlib.Path(
            pytestconfig.invocation_dir, sys.argv[0]
        ).parent.joinpath("buildout")
        package_path = pytestconfig.rootdir
        buildout_cfg = pathlib.Path(tmp_path, "buildout.cfg")
        buildout = u"""
[buildout]
extends =  %(package_path)s/test-4.3.x.cfg
develop =  %(package_path)s
""" % dict(
            package_path=package_path
        )
        with buildout_cfg.open("w") as f:
            f.write(buildout)
        os.chdir(str(tmp_path))
        retcode = subprocess.call([str(buildout_exe), "bootstrap"])
        assert retcode == 0
        try:
            output = subprocess.check_output(
                [str(buildout_exe), "query", "buildout:eggs-directory"]
            )


            self.eggs_directory = output.decode("utf8").split("\n")[-2]
            print "Use eggs directory ", self.eggs_directory

            output = subprocess.check_output(["bin/buildout", "query", "buildout:develop"])
            assert str(package_path).encode("utf8") in output

            output = subprocess.check_output(["bin/buildout", "query", "instance:recipe"])
            assert b"plone.recipe.zope2instance" in output

            output = subprocess.check_output(["bin/buildout", "query", "plonesite:recipe"])
            assert b"collective.recipe.plonesite" in output

        except subprocess.CalledProcessError as e:
            print(e.cmd)
            print(e.output)
            raise e

    def run_buildouts(self, from_version):
        print 
        print "Install collective.ckeditor", from_version
        start = time.time()
        retcode = subprocess.call(
            [
                "bin/buildout",
                "-N",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "buildout:develop=",
                "versions:%s" % from_version,
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()
        total = time.time() - start
        print "in %s seconds" % total
        print()

        print("Setup properties as upgrade setup")
        start = time.time()
        retcode = subprocess.call(
            [
                "bin/buildout",
                "-N",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "instance:zcml=collective.ckeditor:custom-properties.zcml",
                "plonesite:upgrade-profiles=collective.ckeditor:default",
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()
        total = time.time() - start
        print "in %s seconds" % total
        print()
        print("Run upgrade")
        start = time.time()
        retcode = subprocess.call(
            [
                "bin/buildout",
                "-N",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "instance:zcml=collective.ckeditor:migration-registry.zcml",
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()
        total = time.time() - start
        print "in %s seconds" % total

    def check_port(self):
        msg = "There is already another process listening on port %d." % self.port
        assert not check_socket(self.host, self.port), msg

    def start(self):
        self.check_port()
        self.process = subprocess.Popen(["bin/instance", "console"])
        while not check_socket(self.host, self.port):
            time.sleep(0.3)

    def stop(self):
        self.process.terminate()
        # retcode = subprocess.call(["bin/instance", "stop"])
        # assert retcode == 0

    __enter__ = start

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
