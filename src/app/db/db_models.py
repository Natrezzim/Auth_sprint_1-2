import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import class_mapper, ColumnProperty

from src.app.db.db import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Users {self.id}>'


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f'<AuthHistory {self.id}>'


class UserPersonalData(db.Model):
    __tablename__ = 'user_personal_data'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<UserPersonalData {self.id}>'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_type = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Role {self.id}>'


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    permission_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Permission {self.id}>'


class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=True, nullable=False)
    permission_id = db.Column(UUID(as_uuid=True), ForeignKey("permission.id"), unique=True, nullable=False)

    def __repr__(self):
        return f'<RolePermission {self.id}>'


class UserRole(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=True, nullable=False)

    def __repr__(self):
        return f'<UserRole {self.id}>'


class Tokens(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)
