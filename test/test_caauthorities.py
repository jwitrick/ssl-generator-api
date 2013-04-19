# -*- test-case-name: sslgenerator.test.test_caauthorities -*-
from __future__ import absolute_import
from twisted.web.test.test_web import DummyRequest
from twisted.web import resource
from twisted.trial import unittest
from json import JSONEncoder
from mock import Mock, MagicMock, patch
import simplejson
import io

from sslgenerator.v1_0.caauthorities import *


class DummyDELETERequest(DummyRequest):
    method = 'DELETE'
  
    def __init__(self, postpath ,session=None):
        DummyRequest.__init__(self, postpath, session=session)


class DummyPOSTRequest(DummyRequest):
    method = 'POST'
  
    def __init__(self, postpath, content='', headers={}, session=None):
        DummyRequest.__init__(self, postpath, session=session)
        self.content = content
        self.headers = headers


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
        expected_result = {'error':
                           {'code': 404, 'title': 'Not Found',
                           'message': 'The specified CA Authority ' +
                           'not found.\n    test\n    '}}
        encoded = JSONEncoder().encode(expected_result)
        self.assertEquals(encoded, actual_result)

    @patch.object(CAAuthorities, '_get_specified_ca_authority')
    def test_create_caauthority_duplicate(self, mock_get_specified_ca_authority):
        mock_result = {}
        mock_result['ca'] = "test123"
        mock_result['cacert'] = "BLAH....\nBLAH\nBLAH"
        mock_get_specified_ca_authority.return_value = mock_result
        sample_request_data = {}
        ca_authority = {}
        ca_authority['name'] = 'test123'
        ca_authority['days'] = '500' 
        ca_authority['country'] = 'US'
        ca_authority['state/provience'] = 'Virginia'
        ca_authority['locality'] = 'Blacksburg'
        ca_authority['organization_name'] = 'Rackspace'
        ca_authority['organization_unit_name'] = 'Email and Apps'
        ca_authority['common_name'] = 'saopaulo-ca'
        ca_authority['email'] = 'saopaulo-ca'
        sample_request_data['ca_authority'] = ca_authority
        encoded = JSONEncoder().encode(sample_request_data)

        request = DummyPOSTRequest(['test123'], content=io.BytesIO(encoded))
        expected_result = {'error':
                           {'code': 409, 'title': 'Conflict',
                           'message': 'The specified CA Authority ' +
                           'already exists.\n    test123\n    '}}
        encoded_res = JSONEncoder().encode(expected_result)
        cert = CAAuthorities()
        actual_result = cert.render_POST(request)
        self.assertEquals(encoded_res, actual_result)

    def test_create_caauthority_missing_data(self):
        sample_request_data = {}
        headers={'Content-Type': 'application/json'}
        ca_authority = {}
        sample_request_data['ca_authority'] = ca_authority
        encoded = JSONEncoder().encode(sample_request_data)

        request = DummyPOSTRequest(['test123'], content=io.BytesIO(encoded), headers=headers)
        expected_result = {'error':
                           {'code': 400, 'title': 'Bad Request',
                           'message': 'Some required data was not sent.\n    {u\'ca_authority\': {}}\n    '}}
        encoded_res = JSONEncoder().encode(expected_result)
        cert = CAAuthorities()
        actual_result = cert.render_POST(request)
        self.assertEquals(encoded_res, actual_result)

    @patch.object(CAAuthorities, '_create_specified_ca_authority')
    def test_create_caauthority_valid_data(self, mock_create_specified_ca_authority):
        sample_request_data = {}
        ca_authority = {}
        ca_authority['name'] = 'test123'
        ca_authority['days'] = '500' 
        ca_authority['country'] = 'US'
        ca_authority['state/provience'] = 'Virginia'
        ca_authority['locality'] = 'Blacksburg'
        ca_authority['organization_name'] = 'Rackspace'
        ca_authority['organization_unit_name'] = 'Email and Apps'
        ca_authority['common_name'] = 'saopaulo-ca'
        ca_authority['email'] = 'saopaulo-ca'
        sample_request_data['ca_authority'] = ca_authority
        encoded = JSONEncoder().encode(sample_request_data)

        request = DummyPOSTRequest(['test123'], content=io.BytesIO(encoded))
        mock_result = ca_authority
        mock_result['certififate'] = '-----TEST KEY-----'
        mock_create_specified_ca_authority.return_value = mock_result
        expected_results = {}
        expected_results['ca_authority'] = mock_result
        encoded_res = JSONEncoder().encode(expected_results)
        cert = CAAuthorities()
        actual_result = cert.render_POST(request)
        self.assertEquals(encoded_res, actual_result)

    def test_delete_caauthority_missing_data(self):
        request = DummyDELETERequest([])
        expected_result = {'error':
                           {'code': 400, 'title': 'Bad Request',
                           'message': 'Some required data was not sent.\n    \n    '}}
        encoded_res = JSONEncoder().encode(expected_result)
        cert = CAAuthorities()
        actual_result = cert.render_DELETE(request)
        self.assertEquals(encoded_res, actual_result)

    def test_delete_caauthority_non_existant(self):
        request = DummyDELETERequest(['test_non_existant'])
        expected_result = {'error':
                           {'code': 404, 'title': 'Not Found',
                           'message': 'The specified CA Authority not found.\n    test_non_existant\n    '}}
        encoded_res = JSONEncoder().encode(expected_result)
        cert = CAAuthorities()
        actual_result = cert.render_DELETE(request)
        self.assertEquals(encoded_res, actual_result)

    @patch.object(CAAuthorities, '_get_specified_ca_authority')
    def test_delete_caauthority_valid_ca(self, mock_get_specified_ca_authority):
        mock_result = {}
        mock_result['ca_authority'] = {}
        mock_result['ca_authority']['name']= "test_existing_ca"
        mock_result['ca_authority']['certificate'] = "BLAH....\nBLAH\nBLAH"
        mock_get_specified_ca_authority.return_value = mock_result
        request = DummyDELETERequest(['test_existing_ca'])
        cert = CAAuthorities()
        actual_result = cert.render_DELETE(request)
        self.assertIsNone(actual_result)
