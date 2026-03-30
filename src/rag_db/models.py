import uuid
from typing import List
from datetime import datetime

from sqlalchemy import Column, TypeDecorator, func
from sqlalchemy.dialects import mysql
from sqlmodel import Field, SQLModel
from src.auth.utils import verify_password


class GUID(TypeDecorator):
    """Platform-independent GUID type that uses MySQL BINARY(16)."""

    impl = mysql.BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value.bytes
        return uuid.UUID(value).bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(bytes=value)


class User(SQLModel, table=True):

    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(GUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, server_default="user"))
    is_verified: bool = False
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=func.now()))
    

    def __repr__(self):
        return f"<Book {self.username}>"
    
    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)


class QueryLog(SQLModel, table=True):
    
    __tablename__ = "query_logs"
    
    id: uuid.UUID = Field(
        sa_column=Column(GUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(GUID, nullable=False)
    )
    query: str = Field(sa_column=Column(mysql.TEXT, nullable=False))
    response: str = Field(sa_column=Column(mysql.LONGTEXT, nullable=True))
    timestamp: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=func.now()))
    
    def __repr__(self):
        return f"<QueryLog user_id={self.user_id} timestamp={self.timestamp}>"

