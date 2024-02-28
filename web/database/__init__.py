from sqlalchemy.orm import sessionmaker
from .schema import engine

_sess_maker = sessionmaker(bind=engine)

def open_session():
    return _sess_maker()