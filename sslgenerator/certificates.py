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

class Certificates(resource.Resource):

    isLeaf=True
    def render_GET(self, request):
        print "GETTING TO COORRECT PLACE"
        return "HELLO"

    def render_POST(self, request):
        pass

    def render_PUT(self, request):
        pass

    def render_DELETE(self, request):
        pass
