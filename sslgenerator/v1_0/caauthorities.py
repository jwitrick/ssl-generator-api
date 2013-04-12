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

from ..common.config import cfg

class CAAuthorities(resource.Resource):

    isLeaf=True
    def render_GET(self, request):
        """This function will return either:
           1) All CA's if none is specified
           2) Information on the specified CA
        """
        #TODO: Where do I store the list of all CA's
        #      Or do I just query via's app? 
        if request.postpath == [] or request.postpath[0] == '':
             #Need to return all the ca's
             directories = []
             for cdir in os.listdir(os.path.expanduser(str(cfg.general.ca_cert_path))):
                 directories.append(cdir)
             directories.sort()
             print directories
        else:
             print request.postpath
        return "HELLO"

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
