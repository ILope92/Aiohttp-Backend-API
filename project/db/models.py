from sqlalchemy import DATE, VARCHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer, nullable=False,
        unique=True, primary_key=True,
        autoincrement=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=True)
    login = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    date_birth = Column(DATE, nullable=True)

    def __init__(self, first_name, last_name, login, password, date_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password = password
        self.date_birth = date_birth


class Right(BaseModel):
    __tablename__ = 'rights'

    user_id = Column(
        Integer, nullable=False)
    permission = Column(Integer, nullable=False)

    def __init__(self, user_id, permission):
        self.user_id = user_id
        self.permission = permission
