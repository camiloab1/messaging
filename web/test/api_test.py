from util import *
import time
import pytest
from database import open_session
from database.schema import User, Message

@pytest.fixture(scope='function', autouse=True)
def database_prepare():
    session = open_session()
    session.query(Message).delete()
    session.query(User).delete()
    session.commit()


def test_register_doesnt_allow_duplicates():
    request = call_register('Rachel')
    request_json = request.json()
    assert request.status_code == 200
    assert request_json['result'] == 'success'

    request = call_register('Rachel')
    assert request.status_code == 400

def test_messaging_requires_auth():
    request = call_message_create(None, 'Test', 'A content')
    assert request.status_code == 401

    request = call_message_list_received(None)
    assert request.status_code == 401

    request = call_message_list_sent(None)
    assert request.status_code == 401

def test_register_and_send_message():
    request = call_register('Alice')
    request_json = request.json()
    assert request.status_code == 200
    assert request_json['result'] == 'success'

    alice_id = request_json['id']

    request = call_register('Bob')
    request_json = request.json()

    assert request.status_code == 200
    assert request_json['result'] == 'success'

    bob_id = request_json['id']

    request = call_message_create(bob_id, 'Alice', 'A message to Alice, from Bob')
    assert request.status_code == 200
    request_json = request.json()
    assert request_json['result'] == 'success'

    request = call_message_create(alice_id, 'Alice', 'Alice messaging Alice')
    assert request.status_code == 400
    request_json = request.json()
    assert request_json['result'] == 'failure'

    call_register('Wendy')
    request = call_message_create(alice_id, 'Wendy', 'Alice creates a message to Wendy')
    # sleep to force ordering...
    time.sleep(1)
    request = call_message_create(alice_id, 'Wendy', 'Alice creates another message to Wendy')

    request = call_message_list_sent(alice_id)
    assert request.status_code == 200
    request_json = request.json()
    assert request_json['result'] == 'success'
    assert len(request_json['messages']) == 2
    assert request_json['messages'][1]['content'] == 'Alice creates another message to Wendy'

    request = call_message_list_received(alice_id)
    assert request.status_code == 200
    request_json = request.json()
    assert request_json['result'] == 'success'
    assert len(request_json['messages']) == 1
    assert request_json['messages'][0]['content'] == 'A message to Alice, from Bob'


