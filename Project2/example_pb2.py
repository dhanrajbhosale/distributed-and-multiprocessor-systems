# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rexample.proto\"\xcb\x01\n\rBranchRequest\x12\x16\n\tinterface\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x0f\n\x02id\x18\x02 \x01(\x03H\x01\x88\x01\x01\x12\x12\n\x05money\x18\x03 \x01(\x03H\x02\x88\x01\x01\x12\x12\n\x05\x63lock\x18\x04 \x01(\x03H\x03\x88\x01\x01\x12\x11\n\x04type\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x16\n\tbranch_id\x18\x06 \x01(\x03H\x05\x88\x01\x01\x42\x0c\n\n_interfaceB\x05\n\x03_idB\x08\n\x06_moneyB\x08\n\x06_clockB\x07\n\x05_typeB\x0c\n\n_branch_id\"\xd0\x01\n\x0e\x42ranchResponse\x12\x16\n\tinterface\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x13\n\x06result\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07\x62\x61lance\x18\x03 \x01(\x03H\x02\x88\x01\x01\x12\x0f\n\x02id\x18\x04 \x01(\x03H\x03\x88\x01\x01\x12\x12\n\x05\x63lock\x18\x05 \x01(\x03H\x04\x88\x01\x01\x12\x14\n\x07\x65ventid\x18\x06 \x01(\x03H\x05\x88\x01\x01\x42\x0c\n\n_interfaceB\t\n\x07_resultB\n\n\x08_balanceB\x05\n\x03_idB\x08\n\x06_clockB\n\n\x08_eventid27\n\x03RPC\x12\x30\n\x0bMsgDelivery\x12\x0e.BranchRequest\x1a\x0f.BranchResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BRANCHREQUEST']._serialized_start=18
  _globals['_BRANCHREQUEST']._serialized_end=221
  _globals['_BRANCHRESPONSE']._serialized_start=224
  _globals['_BRANCHRESPONSE']._serialized_end=432
  _globals['_RPC']._serialized_start=434
  _globals['_RPC']._serialized_end=489
# @@protoc_insertion_point(module_scope)