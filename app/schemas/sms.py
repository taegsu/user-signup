from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    signup = "signup"
    reset = "reset"


class PhoneNumber(BaseModel):
    phone_number: int
