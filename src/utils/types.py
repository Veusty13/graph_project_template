from typing import TypedDict
from enum import Enum


class Transaction(TypedDict):
    id: int
    step: int
    type: str
    amount: float
    nameorig: str
    oldbalanceorg: float
    newbalanceorig: float
    namedest: str
    oldbalancedest: float
    newbalancedest: float
    isfraud: bool
    isflaggedfraud: bool


class TransactionEdgeInformation(TypedDict):
    id: int
    step: int
    type: str
    amount: float
    oldbalanceorg: float
    newbalanceorig: float
    oldbalancedest: float
    newbalancedest: float
    isfraud: bool
    isflaggedfraud: bool


class TransactionVertexInformation(TypedDict):
    nameorig: str
    namedest: str


class EdgeType(Enum):
    TRANSFER = "TRANSFER"


class VertexType(Enum):
    ACCOUNT = "ACCOUNT"
