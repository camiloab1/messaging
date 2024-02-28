import requests

BASE_ENDPOINT = 'http://localhost:8080'
HANDLER_REGISTER = '/users/register'
HANDLER_MESSAGE_CREATE = '/messages/create'
HANDLER_MESSAGES_LIST_SENT = '/messages/sent/list'
HANDLER_MESSAGES_LIST_RECEIVED = '/messages/received/list'

common_headers = {
    'Content-Type': 'application/json'
}


def call_register(nickname):
    return requests.post(BASE_ENDPOINT + HANDLER_REGISTER, json=dict(nickname=nickname),
                        headers=common_headers)


def call_message_create(x_auth_id, to_nickname, content):
    headers = common_headers
    if x_auth_id:
        headers = common_headers.copy()
        headers['x-auth-id'] = str(x_auth_id)

    return requests.post(BASE_ENDPOINT + HANDLER_MESSAGE_CREATE,
                         json=dict(to_nickname=to_nickname, content=content),
                         headers=headers)


def call_message_list_sent(x_auth_id):
    headers = common_headers
    if x_auth_id:
        headers = common_headers.copy()
        headers['x-auth-id'] = str(x_auth_id)

    return requests.get(BASE_ENDPOINT + HANDLER_MESSAGES_LIST_SENT, headers=headers)


def call_message_list_received(x_auth_id, from_nickname=None):
    headers = common_headers
    if x_auth_id:
        headers = common_headers.copy()
        headers['x-auth-id'] = str(x_auth_id)

    json_params = {}
    if from_nickname:
        json_params['from_nickname'] = from_nickname

    return requests.get(BASE_ENDPOINT + HANDLER_MESSAGES_LIST_RECEIVED,
                         json=json_params,
                         headers=headers)



