
from __future__ import absolute_import
from twisted.web.test.test_web import DummyRequest
from twisted.web import server, resource
from twisted.trial import unittest

from sslgenerator.v1_0.certificates import *


class Certificates_v1_0_TestCase(unittest.TestCase):

    def _listen(self, site):
        return reactor.listenTCP(0, site, interface='127.0.0.1')

    def setUp(self):
        root = resource.Resource()
        root.putChild("certificates", Certificates())
        site = server.Site(root)
        self.port = self._listen(site)
        self.portno = self.port.getHost().port

    def tearDown(self):
        if self.port:
            return self.port.stopListening()

    def getURL(self, path):
        return "http://127.0.0.1:%d/%s" % (self.portno, path)

    def _test_get(self):
        request = DummyRequest(['/v1.0/certificates'])
        print dir(request)
        print request.uri
        print request.postpath
        cert = Certificates()
        print cert.render_GET(request)
        self.assertTrue(False)
