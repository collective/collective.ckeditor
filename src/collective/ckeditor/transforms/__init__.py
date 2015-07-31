# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2006-08-11
# Copyright: quintagroup.com

from Products.PortalTransforms.libtransforms.utils import MissingBinary
modules = [
    'ck_ruid_to_url',
]

g = globals()
transforms = []
for m in modules:
    try:
        ns = __import__(m, g, g, None)
        transforms.append(ns.register())
    except ImportError, e:
        print "Problem importing module %s : %s" % (m, e)
    except MissingBinary, e:
        print e
    except:
        import traceback
        traceback.print_exc()


def initialize(engine):
    for transform in transforms:
        engine.registerTransform(transform)
