import random

from sqlalchemy import create_engine, Table, MetaData, Column, String, Integer, select, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy
from sqlalchemy.exc import ArgumentError, IdentifierError, InvalidRequestError
from typing import AnyStr, Union
from sqlalchemy import MetaData, Table, Column

# Url of the Postgres DB:
DATABASE_URL = 'postgresql+psycopg2://user:password@db_interview_container/app_db'

# Initialize SqlAlchemy instance
metadata = MetaData()
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
session = SessionLocal()

# Clears all previous tables in SqlAlchemy Core
session.expire_all()
Base.metadata.drop_all(bind=engine)


# clients = Table('clients', metadata,
#                 Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
#                 Column('name', String),
#                 Column('balance', Float))

class Client(Base):
    """
    Clients Table definition for SqlAlchemy
    """
    __tablename__ = "clients"

    # Fields for Clients table
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    balance = Column(Float)


Base.metadata.create_all(bind=engine)
session.commit()


def get_client_balance(client_id: int) -> Union[float, None]:
    try:
        clients = session.query(Client).filter(Client.id == client_id)
    except (sqlalchemy.exc.ArgumentError, sqlalchemy.exc.InvalidRequestError):
        return None

    if len(list(clients)) > 1:
        raise ValueError('Request to clients table returned more than 1 row')
    for row in clients:
        return row.balance


def add_client(client_name: AnyStr, client_balance=0.0) -> int:
    """
    Add new Client to the clients table
    :param client_name: Name of the client
    :param client_balance:
    :return: int, Id of the client in the Data base
    """
    session = SessionLocal()
    client = Client(name=client_name, balance=client_balance)

    session.add(client)
    session.flush()
    session.commit()
    session.refresh(client)

    client_id = client.id
    print(f'--- Client id is {client_id} ---')
    return client_id


def update_client_balance(client_id: int, new_balance: float):
    """
    Updates client's balance and sets new value for the balance
    :param client_id: Id of the client
    :param new_balance: new balance to set
    """
    try:
        session.query(Client).filter(Client.id == client_id). \
            update({'balance': new_balance})
        session.commit()
        return True
    except (sqlalchemy.exc.ArgumentError, sqlalchemy.exc.InvalidRequestError):
        return None


def add_to_balance(client_id: int, amount: float, negative=False):
    """
    Takes or adds some amount from/to client's current balance
    :param negative: flag if it is needed to take away or to add to balance
    :param client_id: Id of the client
    :param amount: amount to take/add from/to the balance
    """

    try:
        # Get client's current balance
        client_balance = get_client_balance(client_id)

        if client_balance is not None:

            # Tries to take an amount from client's balance
            if negative:
                new_client_balance = client_balance - amount

                # Raise an Error if client got negative balance
                if new_client_balance < 0:
                    raise ValueError(f'Negative balance after transaction for client with '
                                     f'client_id={client_id}')

            # Adds amount to client's balance
            else:
                new_client_balance = client_balance + amount

            # Update client's balance in the Db Table
            update_client_balance(client_id, new_client_balance)
            return True

    except ValueError:
        return None
