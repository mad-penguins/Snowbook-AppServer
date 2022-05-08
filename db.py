from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite+pysqlite:///snowbook.sqlite3", echo=True, future=True)
Base = declarative_base()


def getSession():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    username = Column(Text, nullable=False)
    passhash = Column(Text, nullable=False)

    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    user_id = Column(Integer, nullable=False)
    token = Column(Text, nullable=False)

    created = Column(DateTime, nullable=False)
    used = Column(DateTime, nullable=False)


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    user_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    text = Column(Text, nullable=False)

    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)

    
def start_db():
    Base.metadata.create_all(engine)


def _add(some):
    session = getSession()

    session.add(some)
    session.commit()

    session.close()

def createNewUser(username, passhash):
    d = datetime.now()

    user = User(username=username, passhash=passhash, created=d, updated=d)

    _add(user)

    return user


def createNewToken(user_id, token):
    d = datetime.now()

    token = Token(user_id=user_id, token=token, created=d, used=d)

    _add(token)

    return token


def createNewNote(user_id, title, text):
    d = datetime.now()

    note = Note(user_id=user_id, title=title, text=text, created=d, updated=d)

    _add(note)

    return note


def getById(obj, ID):
    session = getSession()

    if obj is User:
        response = session.query(User).filter_by(id=ID).first()
    elif obj is Token:
        response = session.query(Token).filter_by(id=ID).first()
    elif obj is Note:
        response = session.query(Note).filter_by(id=ID).first()

    session.close()

    return response


def getUser(username):
    session = getSession()
    response = session.query(User).filter_by(username=username).first()

    session.close()

    return response


def getToken(token):
    session = getSession()
    response = session.query(Token).filter_by(token=token).first()

    session.close()

    return response


def getAllNotes(user):
    session = getSession()
    response = session.query(Note).filter_by(user_id=user.id).all()

    session.close()

    return response


def update(some):
    some.updated = datetime.now()
    _add(some)


def delete(some):
    session = getSession()
    session.delete(some)
    session.commit()
    session.close()


def main():
    start_db()


if __name__ == '__main__':
    main()
