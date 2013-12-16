from __future__ import absolute_import
from twisted.web import server, resource
from twisted.application import service, internet
from twisted.internet import reactor, threads
from twisted.python.failure import Failure as failure
from twisted.web.http_headers import Headers
from twisted.python import log
from pprint import pprint
from json import JSONEncoder
from datetime import datetime
import json
import imp
import importlib

from sslgenerator.common.config import cfg

VERSION = "v1.0"
routes = cfg.v1_0_routes
mods = []

class V1_0(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)
#        print routes
        for k, v in routes.iteritems():
#            log.msg(k)
#            log.msg(type(k))
            mod = importlib.import_module(k)
            c = getattr(mod, v)()
            c_route = k.split('.')[-1]
            self.putChild(c_route, c)


# vim:et:fdm=marker:sts=4:sw=4:ts=4
