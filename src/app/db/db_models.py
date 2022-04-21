import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.db import db


class UserData(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<UserData {self.login}>'


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("user_data.id"), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'<AuthHistory {self.login}>'


class UserPersonalData(db.Model):
    __tablename__ = 'user_personal_data'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("user_data.id"), nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<UserPersonalData {self.login}>'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_type = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Role {self.login}>'


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    permission_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Permission {self.login}>'


class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=True, nullable=False)
    permission_id = db.Column(UUID(as_uuid=True), ForeignKey("permission.id"), unique=True, nullable=False)

    def __repr__(self):
        return f'<RolePermission {self.login}>'


class UserRole(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("user_data.id"), unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=True, nullable=False)

    def __repr__(self):
        return f'<UserRole {self.login}>'
