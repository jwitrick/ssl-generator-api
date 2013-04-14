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
import os

from ..errors import *
from ..common.config import cfg

class CAAuthorities(resource.Resource):

    isLeaf=True
    def render_GET(self, request):
        """This function will return either:
           1) All CA's if none is specified
           2) Information on the specified CA
        """
        directories = []
        result = {}
        if request.postpath == [] or request.postpath[0] == '':
            directories = self._get_ca_authorities()
            result['code'] = '200'
            result['caauthorities'] = directories
        else:
            #TODO: Need to get informatino about the specified va authority
            #The return will have 
            #  1) The name of the CA
            #  2) The key (or whatever the distributed one is)
            #  3) all other information
            try:
                result['code'] = '200'
                result['caauthority'] = self._get_specified_ca_authority(request.postpath[0]) 
                print request.postpath
            except CAAuthorityNotFound as canf:
                request.setResponseCode(canf.code)
                error = {}
                error['code'] = canf.code
                error['title'] = canf.title
                error['message'] = canf.message
                return {'error': error}
#                return {'error': {'code': canf.code, 'title': canf.title, 'message': canf.message]}}
        return result

    def _get_ca_authorities(self):
        directories = []
        if os.path.exists(os.path.expanduser(str(cfg.general.ca_cert_path))):
            for cdir in os.listdir(os.path.expanduser(str(cfg.general.ca_cert_path))):
                directories.append(cdir)
            directories.sort()
        return directories

    def _get_specified_ca_authority(self, ca_authority):
        specified_ca_path = os.path.join(str(cfg.general.ca_cert_path), ca_authority)
        if not os.path.exists(specified_ca_path):
            raise CAAuthorityNotFound(ca_authority=ca_authority)
        return False

    def render_POST(self, request):
        pass

    def render_PUT(self, request):
        pass

    def render_DELETE(self, request):
        pass


    def _format_response(self, response_obj, format_type=None):
        if format_type == None:
            format_type = 'json'
        result = {}
        result['cacertificates'] = []
