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

from .v1_0.certificates import *


class V1_0(resource.Resource):

#    isLeaf = True

    def __init__(self):
        print "INTO constructor"
        resource.Resource.__init__(self)
        self.putChild('certificates', Certificates())
