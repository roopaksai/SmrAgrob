from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from bson import ObjectId
from enum import Enum


@dataclass
class HelloWorldInput:
    name: str


@dataclass
class Output:
    output_message: str = field(default_factory=lambda: "")
    output_details: dict = field(default_factory=lambda: {})
    output_status: str = field(default_factory=lambda: "SUCCESS")


@dataclass
class UserType(Enum):
    emp = "emp"
    user = "user"
    admin = "admin"
    super = "super"


@dataclass
class User:
    email: str
    password: str
    name: Optional[str] = None
    _id: Optional[ObjectId] = None
    phoneNumber: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    user_type: UserType = field(default_factory=lambda: UserType.user.value)


@dataclass
class UserAuthInput:
    action: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phoneNumber: Optional[str] = None
    user_type: UserType = field(default_factory=lambda: UserType.user.value)
