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

from .errors import *
from .common.config import cfg
from .v1_0.certificates import *
from .v1_0.caauthorities import *

VERSION = "v1.0"

class V1_0(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('certificate', Certificates())
        self.putChild('certificates', Certificates())
        self.putChild('caauthorities', CAAuthorities())
        self.putChild('caauthority', CAAuthorities())
