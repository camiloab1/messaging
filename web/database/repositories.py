from . import open_session
from .schema import User, Message
from typing import List

class UserRepository:

    def __init__(self, session=None) -> None:
        if not session:
            session = open_session()

        self.session = session


    def get_by_nickname(self, nickname):
        return self.session.query(User).filter(User.nickname == nickname).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def create_and_save(self, **args):
        new_user = User(**args)
        self.session.add(new_user)
        self.session.commit()

        return new_user


class MessageRepository:
    def __init__(self, session=None) -> None:
        if not session:
            session = open_session()

        self.session = session

    def get_by_sender(self, sender_id) -> List[Message]:
        return self.session.query(Message).filter(
            Message.sender_id==sender_id).order_by(Message.timestamp).all()

    def get_by_recipient(self, recipient_id) -> List[Message]:
        return self.session.query(Message).filter(
            Message.recipient_id==recipient_id).order_by(Message.timestamp).all()

    def get_by_sender_and_recipient(self, sender_id, recipient_id) -> List[Message]:
        return self.session.query(Message).filter(
            Message.sender_id==sender_id,
            Message.recipient_id==recipient_id).order_by(Message.timestamp).all()

    def create_and_save(self, **args) -> Message:
        new_message = Message(**args)
        self.session.add(new_message)
        self.session.commit()

        return new_message