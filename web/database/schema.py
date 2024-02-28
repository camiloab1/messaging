from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, declarative_base
from sqlalchemy.sql import func
from config import DATABASE_URI

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    nickname = mapped_column(String, unique=True, nullable=False, index=True)

class Message(Base):
    __tablename__ = 'messages'

    id = mapped_column(Integer, primary_key=True)
    content = mapped_column(String)
    sender_id = mapped_column(Integer, ForeignKey('users.id'), index=True)
    recipient_id = mapped_column(Integer, ForeignKey('users.id'), index=True)
    timestamp = mapped_column(DateTime, server_default=func.now())

    sender = relationship('User', foreign_keys=[sender_id])
    recipient = relationship('User', foreign_keys=[recipient_id])


engine = create_engine(DATABASE_URI)

def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)
