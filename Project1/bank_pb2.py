# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bank.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nbank.proto\"=\n\rBranchRequest\x12\x11\n\tinterface\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x03\x12\r\n\x05money\x18\x03 \x01(\x03\"D\n\x0e\x42ranchResponse\x12\x11\n\tinterface\x18\x01 \x01(\t\x12\x0e\n\x06result\x18\x02 \x01(\t\x12\x0f\n\x07\x62\x61lance\x18\x03 \x01(\x03\x32:\n\x06\x42ranch\x12\x30\n\x0bMsgDelivery\x12\x0e.BranchRequest\x1a\x0f.BranchResponse\"\x00')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bank_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BRANCHREQUEST']._serialized_start=14
  _globals['_BRANCHREQUEST']._serialized_end=75
  _globals['_BRANCHRESPONSE']._serialized_start=77
  _globals['_BRANCHRESPONSE']._serialized_end=145
  _globals['_BRANCH']._serialized_start=147
  _globals['_BRANCH']._serialized_end=205
# @@protoc_insertion_point(module_scope)