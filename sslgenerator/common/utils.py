import json
from json import JSONEncoder


def error_formatter(exception, format_type=None):
    if format_type is None:
        format_type = 'json'
    if format_type == 'json':
        result = {}
        result['error'] = {}
        result['error']['code'] = exception.code
        result['error']['title'] = exception.title
        result['error']['message'] = exception.message
        return JSONEncoder().encode(result)
