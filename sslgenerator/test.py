from __future__ import absolute_import
from twisted.web import server, resource
from pprint import pprint
from twisted.internet import reactor
from twisted.python.failure import Failure as failure
from twisted.web.http_headers import Headers 
from json import JSONEncoder
import re
import os
from .errors import *
from .common.config import cfg

admin_token = str(cfg.general.admin_token)

class Root(resource.Resource):

    def render_GET(self, request):
        print request


    def getChild(self, name, request):
        if name == "":
            return self
        else:
            pass

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        try:
            _check_admin_token(request)
        except UnauthorizedToken as ut:
            request.setResponseCode(ut.code)
            return error_formatter(ut)
        version = None
        try:
            version = get_url_version(request.uri)
        except UnsupportedVersion as uv:
            request.setResponseCode(uv.code)
            return error_formatter(uv)
        except Exception, exception:
            request.setResponseCode(404)
            return ""
        return "<html>Hello, world!</html>"

VERSIONS = ['1.0']

def _check_admin_token(request):
    token = request.getHeader('x-auth-token')
    if admin_token.lower() == 'admin':
        return True
    if token != None:
        if token.lower() == admin_token.lower():
          return True
    raise UnauthorizedToken(admin_token=token)

def get_url_version(url):
    for version in VERSIONS:
        reg_string = "^\/v%s"%version
        reg = re.compile(reg_string)
        res = reg.findall(url)
        if len(res) == 1:
            return version
    raise UnsupportedVersion(url_id=url)

def error_formatter(exception, format_type=None):
    if format_type == None:
        format_type = 'json'
    if format_type == 'json':
        result = {}
        result['error'] = {}
        result['error']['code'] = exception.code
        result['error']['title'] = exception.title
        result['error']['message'] = exception.message
        return JSONEncoder().encode(result)
    

site = server.Site(Simple())
reactor.listenTCP(8080, site, interface='localhost')
#reactor.listenTCP(8080, site)
reactor.run()
