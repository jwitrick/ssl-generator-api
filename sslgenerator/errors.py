
from json import JSONEncoder
import re


class Error(StandardError):
    """Base error class.

    Child classes should define an HTTP status code, title, and doc string.
    """
    code = None
    title = None

    def __init__(self, message=None, **kwargs):
        """Use the doc string as the error message by default."""

        try:
            message = self._build_message(message, **kwargs)
        except KeyError as e:
            # if you see this warning in your logs, please raise a bug report
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise e
            else:
                LOG.warning('missing exception kwargs (programmer error)')
                message = self.__doc__

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Builds and returns an exception message.

        :raises: KeyError given insufficient kwargs

        """
        return message or self.__doc__ % kwargs

    def __str__(self):
        """Cleans up line breaks and indentation from doc strings."""
        string = super(Error, self).__str__()
        string = re.sub('[ \n]+', ' ', string)
        string = string.strip()
        return string


class UnsupportedVersion(Error):
    """Recieved an unsupported api version identifier.

    %(url_id)s

    """
    code = 400
    title = "Bad Request"

    def __init__(self, url_id):
        super(UnsupportedVersion, self).__init__(url_id=url_id)


class UnauthorizedToken(Error):
    """Recieved an incorrect x-auth-token.
    %(admin_token)s
    """
    code = 401
    title = "Unauthorized"

    def __init__(self, admin_token):
        super(UnauthorizedToken, self).__init__(admin_token=admin_token)


class RouteNotSupported(Error):
    """The specified route is not supported.
    %(route)s
    """
    code = 405
    title = "Method Not Allowed"

    def __init__(self, route):
        super(RouteNotSupported, self).__init__(route=route)


class CAAuthorityNotFound(Error):
    """The specified CA Authority not found.
    %(ca_authority)s
    """
    code = 404
    title = "Not Found"

    def __init__(self, ca_authority):
        super(CAAuthorityNotFound, self).__init__(ca_authority=ca_authority)


class DuplicateCAAuthority(Error):
    """The specified CA Authority already exists.
    %(ca_authority)s
    """
    code = 409
    title = 'Conflict'

    def __init__(self, ca_authority):
        super(DuplicateCAAuthority, self).__init__(ca_authority=ca_authority)


class MissingData(Error):
    """Some required data was not sent.
    %(sent_data)s
    """
    code = 400
    title = 'Bad Request'

    def __init__(self, sent_data):
        super(MissingData, self).__init__(sent_data=sent_data)
