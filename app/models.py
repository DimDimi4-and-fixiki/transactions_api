from pydantic import BaseModel
from typing import Union, AnyStr


class Client(BaseModel):
    """
    Clients Model definition for API requests
    """

    # Fields for Clients model
    name: str
    balance: float = 0.0


class Transaction(BaseModel):
    """
    Transactions Model
    """

    first_client_id: int
    second_client_id: int
    amount: float

