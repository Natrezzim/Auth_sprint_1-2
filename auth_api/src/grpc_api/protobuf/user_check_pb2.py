# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user_check.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10user_check.proto\x12\tcheckuser\"(\n\x10\x43heckUserRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\"*\n\tCheckUser\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\r\n\x05roles\x18\x02 \x03(\t*\x1f\n\x08RoleUser\x12\t\n\x05\x41\x44MIN\x10\x00\x12\x08\n\x04USER\x10\x01\x32S\n\rCheckAuthUser\x12\x42\n\x0bGetAuthInfo\x12\x1b.checkuser.CheckUserRequest\x1a\x14.checkuser.CheckUser\"\x00\x62\x06proto3')

_ROLEUSER = DESCRIPTOR.enum_types_by_name['RoleUser']
RoleUser = enum_type_wrapper.EnumTypeWrapper(_ROLEUSER)
ADMIN = 0
USER = 1


_CHECKUSERREQUEST = DESCRIPTOR.message_types_by_name['CheckUserRequest']
_CHECKUSER = DESCRIPTOR.message_types_by_name['CheckUser']
CheckUserRequest = _reflection.GeneratedProtocolMessageType('CheckUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHECKUSERREQUEST,
  '__module__' : 'user_check_pb2'
  # @@protoc_insertion_point(class_scope:checkuser.CheckUserRequest)
  })
_sym_db.RegisterMessage(CheckUserRequest)

CheckUser = _reflection.GeneratedProtocolMessageType('CheckUser', (_message.Message,), {
  'DESCRIPTOR' : _CHECKUSER,
  '__module__' : 'user_check_pb2'
  # @@protoc_insertion_point(class_scope:checkuser.CheckUser)
  })
_sym_db.RegisterMessage(CheckUser)

_CHECKAUTHUSER = DESCRIPTOR.services_by_name['CheckAuthUser']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ROLEUSER._serialized_start=117
  _ROLEUSER._serialized_end=148
  _CHECKUSERREQUEST._serialized_start=31
  _CHECKUSERREQUEST._serialized_end=71
  _CHECKUSER._serialized_start=73
  _CHECKUSER._serialized_end=115
  _CHECKAUTHUSER._serialized_start=150
  _CHECKAUTHUSER._serialized_end=233
# @@protoc_insertion_point(module_scope)
