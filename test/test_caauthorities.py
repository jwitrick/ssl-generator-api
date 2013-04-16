# -*- test-case-name: sslgenerator.test.test_caauthorities -*-
from __future__ import absolute_import
from twisted.web.test.test_web import DummyRequest
from twisted.web import server, resource
from twisted.trial import unittest
import os
from json import JSONEncoder
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
        expected_result['ca_authorities'] = ['ca1', 'ca2', 'ca3']
        encoded = JSONEncoder().encode(expected_result)
        self.assertEquals(encoded, actual_result)

    @patch.object(CAAuthorities, '_get_ca_authorities')
    def test_get_list_ca_certs_empty_dir(self, mock_get_ca_authorities):
        mock_get_ca_authorities.return_value = []
        request = DummyRequest([''])
        cert = CAAuthorities()
        actual_result = cert.render_GET(request)
        expected_result = {}
        expected_result['ca_authorities'] = []
        encoded = JSONEncoder().encode(expected_result)
        self.assertEquals(encoded, actual_result)

    @patch.object(CAAuthorities, '_get_specified_ca_authority')
    def test_get_specified_ca_exists(self, mock_get_specified_ca_authority):
        mock_result = {}
        mock_result['ca'] = "test123"
        mock_result['cacert'] = "BLAH....\nBLAH\nBLAH"
        mock_get_specified_ca_authority.return_value = mock_result
        request = DummyRequest(['test123'])
        cert = CAAuthorities()
        actual_result = cert.render_GET(request)
        expected_result = {'ca_authority': mock_result}
        encoded = JSONEncoder().encode(expected_result)
        self.assertEquals(encoded, actual_result)

    def test_get_specified_ca_expect_exception(self):
        request = DummyRequest(['test'])
        cert = CAAuthorities()
        actual_result = cert.render_GET(request)
        expected_result = {'error': {'code':404, 'title': 'Not Found', 'message': 'The specified Ca Authority not found.\n    test\n    '}}
        encoded = JSONEncoder().encode(expected_result)
        self.assertEquals(encoded, actual_result)

    def test_create_tenant_duplicate(self):
        sample_request_data = {}
        sample_request_data['ca_authority'] = {}
        sample_request_data['ca_authority']['name'] = 'test123'
        sample_request_data['ca_authority']['description'] = 'A CA authority to handle all certs for test'

        self.assertTrue(False)

    def test_create_tenant_missing_data(self):
        self.assertTrue(False)

    def test_create_tenant_valid_data(self):
        self.assertTrue(False)

    
