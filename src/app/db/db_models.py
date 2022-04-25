import datetime
import uuid
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import class_mapper, ColumnProperty

from src.app.db.db import db


@dataclass
class Users(db.Model):
    __tablename__ = 'users'

    id: uuid.uuid4()
    username: str
    password: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Users {self.id}>'


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    user_agent: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f'<AuthHistory {self.id}>'

@dataclass
class UserPersonalData(db.Model):
    __tablename__ = 'user_personal_data'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    email: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<UserPersonalData {self.id}>'


@dataclass
class Role(db.Model):
    __tablename__ = 'role'

    id: uuid.uuid4()
    role_type: str
    description: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_type = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Role {self.id}>'


@dataclass
class Permission(db.Model):
    __tablename__ = 'permission'

    id: uuid.uuid4()
    permission_id: int
    description: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    permission_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Permission {self.id}>'


@dataclass
class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id: uuid.uuid4()
    role_id: uuid.uuid4()
    permission_id: uuid.uuid4()

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=True, nullable=False)
    permission_id = db.Column(UUID(as_uuid=True), ForeignKey("permission.id"), unique=True, nullable=False)

    def __repr__(self):
        return f'<RolePermission {self.id}>'


@dataclass
class UserRole(db.Model):
    __tablename__ = 'user_role'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    role_id: uuid.uuid4()

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=True, nullable=False)

    def __repr__(self):
        return f'<UserRole {self.id}>'


@dataclass
class Tokens(db.Model):
    __tablename__ = 'tokens'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    refresh_token: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)
