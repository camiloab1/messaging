from flask import jsonify, request, abort
from typing import AnyStr

def json_response_failure(reason: AnyStr):
    response = jsonify(dict(result='failure', reason=reason))
    response.status_code = 400
    return response


def json_response_success(body=None):
    if not body:
        body = {}
    body['result'] = 'success'
    return jsonify(body)


def validate_required_header(header_name):
    header_value = request.headers.get(header_name, None)
    if not header_value:
        abort(401)

    return header_value