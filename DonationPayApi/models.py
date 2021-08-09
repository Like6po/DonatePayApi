import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    avatar: str
    balance: int
    cashout_sum: int


class Vars(BaseModel):
    user_ip: Optional[str]
    name: str
    comment: str


class Transaction(BaseModel):
    id: int
    what: str
    sum: float
    to_cash: Optional[str]
    to_pay: Optional[str]
    commission: float
    status: str
    type: str
    vars: Vars
    comment: str
    created_at: datetime.datetime


class ListOfTransactions(list):
    def __init__(self, data):
        super().__init__()
        for d in data:
            self.append(Transaction.parse_obj(d))
