from __future__ import absolute_import
from twisted.web.test.test_web import DummyRequest
from twisted.web import server, resource
from twisted.trial import unittest

from sslgenerator.v1_0.caauthorities import *

class CAAuthorities_v1_0_TestCase(unittest.TestCase):

    def setUp(self):
        root = resource.Resource()
        root.putChild("caauthorities", CAAuthorities())

    def test_get(self):
        print "PRINTING HEADER"
        request = DummyRequest(['/v1.0/caauthorities'])
        request.setHeader("X-Auth-Token","hello")
        print "hello"
        print dir(request)
        print request.uri
        print request.postpath
        print request.getAllHeaders()
        print request.getHeader('x-auth-token')
        cert = CAAuthorities()
        print cert.render_GET(request)
        self.assertTrue(False)
