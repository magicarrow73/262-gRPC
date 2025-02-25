# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: chat.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'chat.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"T\n\x11\x43reateUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x17\n\x0fhashed_password\x18\x02 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x03 \x01(\t\"G\n\x12\x43reateUserResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\"9\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x17\n\x0fhashed_password\x18\x02 \x01(\t\"X\n\rLoginResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x14\n\x0cunread_count\x18\x03 \x01(\x05\x12\x10\n\x08username\x18\x04 \x01(\t\"!\n\rLogoutRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"1\n\x0eLogoutResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"5\n\x10ListUsersRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0f\n\x07pattern\x18\x02 \x01(\t\"2\n\x08UserInfo\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\"d\n\x11ListUsersResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1d\n\x05users\x18\x03 \x03(\x0b\x32\x0e.chat.UserInfo\x12\x0f\n\x07pattern\x18\x04 \x01(\t\"G\n\x12SendMessageRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"6\n\x13SendMessageResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"K\n\x13ReadMessagesRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x13\n\x0bonly_unread\x18\x02 \x01(\x08\x12\r\n\x05limit\x18\x03 \x01(\x05\"k\n\x0b\x43hatMessage\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x17\n\x0fsender_username\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\x12\x13\n\x0bread_status\x18\x05 \x01(\x05\"\\\n\x14ReadMessagesResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12#\n\x08messages\x18\x03 \x03(\x0b\x32\x11.chat.ChatMessage\">\n\x15\x44\x65leteMessagesRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x13\n\x0bmessage_ids\x18\x02 \x03(\x05\"P\n\x16\x44\x65leteMessagesResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x15\n\rdeleted_count\x18\x03 \x01(\x05\"%\n\x11\x44\x65leteUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"5\n\x12\x44\x65leteUserResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"$\n\x10SubscribeRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"2\n\x0fIncomingMessage\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t2\xca\x04\n\x0b\x43hatService\x12?\n\nCreateUser\x12\x17.chat.CreateUserRequest\x1a\x18.chat.CreateUserResponse\x12\x30\n\x05Login\x12\x12.chat.LoginRequest\x1a\x13.chat.LoginResponse\x12\x33\n\x06Logout\x12\x13.chat.LogoutRequest\x1a\x14.chat.LogoutResponse\x12<\n\tListUsers\x12\x16.chat.ListUsersRequest\x1a\x17.chat.ListUsersResponse\x12\x42\n\x0bSendMessage\x12\x18.chat.SendMessageRequest\x1a\x19.chat.SendMessageResponse\x12\x45\n\x0cReadMessages\x12\x19.chat.ReadMessagesRequest\x1a\x1a.chat.ReadMessagesResponse\x12K\n\x0e\x44\x65leteMessages\x12\x1b.chat.DeleteMessagesRequest\x1a\x1c.chat.DeleteMessagesResponse\x12?\n\nDeleteUser\x12\x17.chat.DeleteUserRequest\x1a\x18.chat.DeleteUserResponse\x12<\n\tSubscribe\x12\x16.chat.SubscribeRequest\x1a\x15.chat.IncomingMessage0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEUSERREQUEST']._serialized_start=20
  _globals['_CREATEUSERREQUEST']._serialized_end=104
  _globals['_CREATEUSERRESPONSE']._serialized_start=106
  _globals['_CREATEUSERRESPONSE']._serialized_end=177
  _globals['_LOGINREQUEST']._serialized_start=179
  _globals['_LOGINREQUEST']._serialized_end=236
  _globals['_LOGINRESPONSE']._serialized_start=238
  _globals['_LOGINRESPONSE']._serialized_end=326
  _globals['_LOGOUTREQUEST']._serialized_start=328
  _globals['_LOGOUTREQUEST']._serialized_end=361
  _globals['_LOGOUTRESPONSE']._serialized_start=363
  _globals['_LOGOUTRESPONSE']._serialized_end=412
  _globals['_LISTUSERSREQUEST']._serialized_start=414
  _globals['_LISTUSERSREQUEST']._serialized_end=467
  _globals['_USERINFO']._serialized_start=469
  _globals['_USERINFO']._serialized_end=519
  _globals['_LISTUSERSRESPONSE']._serialized_start=521
  _globals['_LISTUSERSRESPONSE']._serialized_end=621
  _globals['_SENDMESSAGEREQUEST']._serialized_start=623
  _globals['_SENDMESSAGEREQUEST']._serialized_end=694
  _globals['_SENDMESSAGERESPONSE']._serialized_start=696
  _globals['_SENDMESSAGERESPONSE']._serialized_end=750
  _globals['_READMESSAGESREQUEST']._serialized_start=752
  _globals['_READMESSAGESREQUEST']._serialized_end=827
  _globals['_CHATMESSAGE']._serialized_start=829
  _globals['_CHATMESSAGE']._serialized_end=936
  _globals['_READMESSAGESRESPONSE']._serialized_start=938
  _globals['_READMESSAGESRESPONSE']._serialized_end=1030
  _globals['_DELETEMESSAGESREQUEST']._serialized_start=1032
  _globals['_DELETEMESSAGESREQUEST']._serialized_end=1094
  _globals['_DELETEMESSAGESRESPONSE']._serialized_start=1096
  _globals['_DELETEMESSAGESRESPONSE']._serialized_end=1176
  _globals['_DELETEUSERREQUEST']._serialized_start=1178
  _globals['_DELETEUSERREQUEST']._serialized_end=1215
  _globals['_DELETEUSERRESPONSE']._serialized_start=1217
  _globals['_DELETEUSERRESPONSE']._serialized_end=1270
  _globals['_SUBSCRIBEREQUEST']._serialized_start=1272
  _globals['_SUBSCRIBEREQUEST']._serialized_end=1308
  _globals['_INCOMINGMESSAGE']._serialized_start=1310
  _globals['_INCOMINGMESSAGE']._serialized_end=1360
  _globals['_CHATSERVICE']._serialized_start=1363
  _globals['_CHATSERVICE']._serialized_end=1949
# @@protoc_insertion_point(module_scope)
