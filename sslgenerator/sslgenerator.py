from __future__ import absolute_import
from twisted.web import server, resource
from twisted.application import service, internet
from twisted.internet import reactor, ssl
from twisted.python.failure import Failure as failure
from twisted.web.http_headers import Headers
from twisted.python import log
from pprint import pprint
from json import JSONEncoder
from datetime import datetime
import json
import re
import os
import sys
from sslgenerator.common.utils import *
from sslgenerator.errors import *
from sslgenerator.common.config import cfg
#from certificates import *
from sslgenerator.v_1_0 import *

admin_token = str(cfg.general.admin_token)
host_ip = str(cfg.general.listen_ip)
host_port = int(cfg.general.listen_port)
non_ssl_port = int(cfg.general.non_ssl_port)

#routes = json.loads(cfg.routes.builtin_routes)


class Root(resource.Resource):

    def getChild(self, name, request):
        if name == '':
            return self
        else:
            try:
                _check_admin_token(request)
                if name == "v1.0":
                    return V1_0()
                if name in cfg.routes.keys():
                    return resource.Resource.getChild(self, name, request)
                raise RouteNotSupported(route=name)
            except UnauthorizedToken as ut:
                request.setResponseCode(ut.code)
                return error_formatter(ut)
            except RouteNotSupported as rns:
                request.setResponseCode(rns.code)
                return error_formatter(rns)
            except Exception as e:
                print e
                print "HANDLING EXCEPTION"
                return ""


def _check_admin_token(request):
    whitelisted_routes = ["pxe", "kickstart"]
    token = request.getHeader('x-auth-token')
    if request.postpath[0] in whitelisted_routes:
        return True
    elif admin_token.lower() == 'admin':
        return True
    if token is not None:
        if token.lower() == admin_token.lower():
            return True
    raise UnauthorizedToken(admin_token=token)


def get_url_version(url):
    versions = json.loads(cfg.versions.supported_versions)
    if url[0] != '/':
        url = "/" + url
    specified_version = url.split('/', 2)[1]
    if versions in specified_version:
        return specified_version
    raise UnsupportedVersion(url_id=url)


def main():
    root = Root()
    root.putChild("v1", V1_0())
#    for routeName, className in routes.items():
#        root.putChild(routeName, className)
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' % str(datetime.now()))
    app = server.Site(root)
#    reactor.listenSSL(host_port, app,
#                      ssl.DefaultOpenSSLContextFactory(
#            cfg.general.ssl_key, cfg.general.ssl_cert))
    reactor.listenTCP(int(cfg.general.non_ssl_port), app, interface=host_ip)
    reactor.listenTCP(8000, app, interface=host_ip)
    reactor.run()


if __name__ == '__main__':
    main()

else:
    root = Root()
    root.putChild("v1", V1_0())
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' % str(datetime.now()))
    application = service.Application("dave-api")
#    internet.SSLServer(host_port, server.Site(root),
#                  ssl.DefaultOpenSSLContextFactory(
#                    cfg.general.ssl_key, cfg.general.ssl_cert)
#                  ).setServiceParent(application)
    internet.TCPServer(non_ssl_port,
                     server.Site(root)).setServiceParent(application)


# vim:et:fdm=marker:sts=4:sw=4:ts=4
