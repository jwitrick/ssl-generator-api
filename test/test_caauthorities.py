from __future__ import absolute_import
from twisted.web.test.test_web import DummyRequest
from twisted.web import server, resource
from twisted.trial import unittest
import os
from mock import Mock, MagicMock, patch

from sslgenerator.v1_0.caauthorities import *

class CAAuthorities_v1_0_TestCase(unittest.TestCase):

    def setUp(self):
        root = resource.Resource()
        root.putChild("caauthorities", CAAuthorities())

#    def test_get(self):
#        request = DummyRequest(['/v1.0/caauthorities'])
#        request.headers["x-auth-token"] = "hello"
#        cert = CAAuthorities()
#        self.assertTrue(False)

    @patch.object(CAAuthorities, '_get_ca_authorities')
    def test_get_list_ca_certs(self, mock_get_ca_authorities):
        mock_get_ca_authorities.return_value = ['ca1', 'ca2', 'ca3']
        request = DummyRequest([''])
        cert = CAAuthorities()
        actual_result = cert.render_GET(request)
        expected_result = {}
        expected_result['code'] = '200'
        expected_result['caauthorities'] = ['ca1', 'ca2', 'ca3']
        self.assertEquals(expected_result, actual_result)

    @patch.object(CAAuthorities, '_get_ca_authorities')
    def test_get_list_ca_certs_empty_dir(self, mock_get_ca_authorities):
        mock_get_ca_authorities.return_value = []
        request = DummyRequest([''])
        cert = CAAuthorities()
        actual_result = cert.render_GET(request)
        expected_result = {}
        expected_result['code'] = '200'
        expected_result['caauthorities'] = []
        self.assertEquals(expected_result, actual_result)

    def test_get_specified_ca_expect_exception(self):
        request = DummyRequest(['test'])
        cert = CAAuthorities()
        actual_result = cert.render_GET(request)
        expected_result = {'error': {'code':404, 'title': 'Not Found', 'message': 'The specified Ca Authority not found.\n    test\n    '}}
        self.assertEquals(expected_result, actual_result)
