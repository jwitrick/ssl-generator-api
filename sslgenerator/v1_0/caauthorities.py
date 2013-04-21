from __future__ import absolute_import
from twisted.web import resource
import os
import shutil

from ..errors import *
from ..common.config import cfg
from ..common.utils import *


class CAAuthorities(resource.Resource):

    isLeaf = True
    _required_fields = ['name', 'days', 'country', 'state/provience',
                        'locality', 'organization_name', 
                        'organization_unit_name', 'common_name', 'email']

    def render_GET(self, request):
        """This function will return either:
           1) All CA's if none is specified
           2) Information on the specified CA
        """
        directories = []
        result = {}
        if request.postpath == [] or request.postpath[0] == '':
            directories = self._get_ca_authorities()
            result = self._format_ca_authorities(directories, False)
        else:
            try:
                specified_authority = self._get_specified_ca_authority(
                    request.postpath[0])
                result = self._format_ca_authorities(specified_authority)
            except CAAuthorityNotFound as canf:
                request.setResponseCode(canf.code)
                return error_formatter(canf)
        return result

    def _get_ca_authorities(self):
        directories = []
        if os.path.exists(os.path.expanduser(str(cfg.general.ca_cert_path))):
            for cdir in os.listdir(os.path.expanduser(
                    str(cfg.general.ca_cert_path))):
                directories.append(cdir)
            directories.sort()
        return directories

    def _get_specified_ca_authority(self, ca_authority):
        specified_ca_path = os.path.join(os.path.expanduser(
            str(cfg.general.ca_cert_path)), ca_authority)
        if not os.path.exists(specified_ca_path):
            raise CAAuthorityNotFound(ca_authority=ca_authority)
        #TODO: Here I need to call the openssl library to actually
        #  return the information about this ca_authority
        return None

    def _delete_specified_ca_authority(self, ca_authority):
        specified_ca_path = os.path.join(os.path.expanduser(
            str(cfg.general.ca_cert_path)), ca_authority)
        if not os.path.exists(specified_ca_path):
            return True
        else:
            shutil.rmtree(specified_ca_path)
        return True

    def _format_ca_authorities(self, ca_authorities, single=True):
        result = {}
        if single:
            result['ca_authority'] = ca_authorities
        else:
            result['ca_authorities'] = ca_authorities
        return JSONEncoder().encode(result)

    def _check_data_for_required_fields(self, data):
        if data['ca_authority'] is None:
            raise MissingData(sent_data=data) 

        for field in self._required_fields:
            if not field in data['ca_authority'].keys():
                raise MissingData(sent_data=data)
        return True

    def _create_specified_ca_authority(self, data):
        return True

    def render_POST(self, request):
        """This function will attempt to create a new CA Authority.
        If the request is empty will return a MissingData error
        If the ca already exists it will return a DuplicateCAAuthority error.
        If successful it will return json withe CA info.
        """
        ca_authority = {}
        try:
            content = request.content.getvalue()
            if len(content) == 0:
                raise MissingData(sent_data=content) 

            if request.getHeader('content-type') == 'application/json' or request.getHeader('content-type') is None:
                content = json.loads(content)
            else:
                print request.getHeader('content-type')
                print "Unsupported content-type"

            self._check_data_for_required_fields(content)
            specified_ca_authority = content['ca_authority']['name']
            try:
                if self._get_specified_ca_authority(specified_ca_authority) is not None:
                    raise DuplicateCAAuthority(ca_authority=specified_ca_authority)
            except DuplicateCAAuthority as dca:
                request.setResponseCode(dca.code)
                return error_formatter(dca)
            except CAAuthorityNotFound as caaunf:
                pass
            ca_authority = self._create_specified_ca_authority(specified_ca_authority)

        except MissingData as md:
            request.setResponseCode(400)
            return error_formatter(md)
        return self._format_ca_authorities(ca_authority)

    def render_DELETE(self, request):
        """This function will attempt to delete the given CA.
        NOTE: Any certs signed by this CA will not longer be 
        able to authenticate and so unable to renew certs.
        """
        try:
            if request.postpath == [] or request.postpath[0] == '':
                raise MissingData(sent_data='')
            specified_ca_str = request.postpath[0]
            self._get_specified_ca_authority(specified_ca_str)
            if self._delete_specified_ca_authority(specified_ca_str):
                result = request.setResponseCode(204)
                return result
        except MissingData as md:
            request.setResponseCode(md.code)
            return error_formatter(md)
        except CAAuthorityNotFound as canf:
            request.setResponseCode(canf.code)
            return error_formatter(canf)
        return None

