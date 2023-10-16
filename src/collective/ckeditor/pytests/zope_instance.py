import os
import sys
import time
import subprocess
try:
    import pathlib
except ImportError:
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
        buildout_43_cfg = pathlib.Path(tmp_path, "buildout-4.3.x.cfg")
        content = u"""
[buildout]
extends =  %(package_path)s/test-4.3.x.cfg
develop =  %(package_path)s
auto-checkout = 

[instance]
eggs +=
  collective.upgrade
""" % dict(
            package_path=package_path
        )
        with buildout_43_cfg.open("w") as f:
            f.write(content)
        buildout_52_cfg = pathlib.Path(tmp_path, "buildout-5.2.x.cfg")
        content = u"""
[buildout]
extends =  %(package_path)s/test-5.2.x.cfg
develop =  %(package_path)s

[instance]
eggs +=
  Plone [archetypes]
  collective.upgrade
""" % dict(
            package_path=package_path
        )
        with buildout_52_cfg.open("w") as f:
            f.write(content)
        os.chdir(str(tmp_path))
        retcode = subprocess.call([str(buildout_exe), "-c", str(buildout_43_cfg), "bootstrap"])
        assert retcode == 0
        try:
            output = subprocess.check_output(
                [str(buildout_exe), "-c", str(buildout_43_cfg), "query", "buildout:eggs-directory"]
            )
            self.eggs_directory = output.decode("utf8").split("\n")[-2]
            print("Use eggs directory ", self.eggs_directory)

            output = subprocess.check_output(["bin/buildout", "-c", str(buildout_52_cfg), "query", "buildout:develop"])
            assert str(package_path).encode("utf8") in output

        except subprocess.CalledProcessError as e:
            print(e.cmd)
            print(e.output)
            raise e
        self.assert_buildout_can_upgrade_via_plonesite(str(buildout_43_cfg))
        self.assert_buildout_can_upgrade_via_plonesite(str(buildout_52_cfg))

    def assert_buildout_can_upgrade_via_plonesite(self, buildout_cfg):
        try:
            output = subprocess.check_output(["bin/buildout", "-c", buildout_cfg, "query", "instance:recipe"])
            assert b"plone.recipe.zope2instance" in output

            output = subprocess.check_output(["bin/buildout", "-c", buildout_cfg, "query", "instance:eggs"])
            assert b"collective.upgrade" in output

            output = subprocess.check_output(["bin/buildout", "-c", buildout_cfg, "query", "plonesite:recipe"])
            assert b"collective.recipe.plonesite" in output
 
        except subprocess.CalledProcessError as e:
            print(e.cmd)
            print(e.output)
            raise e

    def run_buildouts(self):
        print()
        print()
        print("Install collective.ckeditor 4.10.1")
        print("----------------------------------")
        start = time.time()
        retcode = subprocess.call(
            [
                "bin/buildout",
                "-N",
                "-c",
                "buildout-4.3.x.cfg",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "buildout:develop=",
                "versions:collective.ckeditor=4.10.1",
                "versions:collective.plonefinder=1.3.1",
                "versions:collective.quickupload=1.11.1",
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()
        total = time.time() - start
        print("in %s seconds" % total)
        print()
        print()
        print("Non defaut properties as setup for upgrade step to registry")
        print("___________________________________________________________")
        start = time.time()
        retcode = subprocess.call(
            [
                "bin/buildout",
                "-N",
                "-c",
                "buildout-5.2.x.cfg",
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
        print("in %s seconds" % total)
        print()
        print()
        print("Run upgrade")
        print("-----------")
        start = time.time()
        retcode = subprocess.call(
            [
                "bin/buildout",
                "-N",
                "-c",
                "buildout-5.2.x.cfg",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "plonesite:upgrade-profiles=collective.ckeditor:default",
                "plonesite:profiles=collective.quickupload:default",
                "instance:zcml=collective.ckeditor:migration-registry.zcml",
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()
        total = time.time() - start
        print("in %s seconds" % total)

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

    __enter__ = start

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
