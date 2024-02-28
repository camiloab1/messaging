from database import open_session
from database.schema import User, Message
from database.repositories import UserRepository, MessageRepository
from flask import Flask, request
from utils.http import *

handlers = Flask(__name__)

@handlers.route('/users/register', methods=['POST'])
def register():
    nickname = request.json.get('nickname', None)
    if not nickname:
        return json_response_failure('The nickname parameter was not provided')

    repository = UserRepository()
    existing_user = repository.get_by_nickname(nickname)
    if existing_user:
        return json_response_failure('The nickname already exists')

    new_user = repository.create_and_save(nickname=nickname)

    return json_response_success(dict(id=new_user.id))


@handlers.route('/messages/create', methods=['POST'])
def create_message():
    auth_id = int(validate_required_header('x-auth-id'))
    required_parameters = ['to_nickname', 'content']
    for parameter in required_parameters:
        value = request.json.get(parameter, None)
        if not value:
            return json_response_failure('The {} parameter was not provided'.format(parameter))

    to_nickname = request.json['to_nickname']
    content = request.json['content']

    session = open_session()
    user_repository = UserRepository(session)
    recipient = user_repository.get_by_nickname(to_nickname)
    if not recipient:
        return json_response_failure('The desired recipient does not exist')

    if recipient.id == auth_id:
        return json_response_failure('You cannot create a message for yourself')

    message_repository = MessageRepository(session)
    message_repository.create_and_save(content=content, recipient=recipient, sender_id=auth_id)

    return json_response_success()


@handlers.route('/messages/sent/list', methods=['GET'])
def list_sent_messages():
    auth_id = int(validate_required_header('x-auth-id'))
    message_repository = MessageRepository()
    messages = message_repository.get_by_sender(auth_id)

    result = [dict(to_user=m.recipient.nickname, from_user=m.sender.nickname,
                   content=m.content, timestamp=m.timestamp) for m in messages]

    return json_response_success(dict(messages=result))


@handlers.route('/messages/received/list', methods=['GET'])
def list_received_messages():
    # message recipient is the authenticated user
    auth_id = int(validate_required_header('x-auth-id'))

    # optional parameter, to filter for sender
    from_nickname = request.json.get('from_nickname', None)

    session = open_session()
    message_repository = MessageRepository(session)
    if from_nickname:
        user_repository = UserRepository(session)
        from_user = user_repository.get_by_nickname(from_nickname)
        if not from_user:
            return json_response_failure('Sender does not exist')

        messages = message_repository.get_by_sender_and_recipient(from_user.id, auth_id)
    else:
        messages = message_repository.get_by_recipient(auth_id)

    result = [dict(to_user=m.recipient.nickname, from_user=m.sender.nickname,
                   content=m.content, timestamp=m.timestamp) for m in messages]

    return json_response_success(dict(messages=result))


