# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: map.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tmap.proto\x12\tinterface\"%\n\x07Point2D\x12\x0c\n\x01x\x18\x01 \x01(\x01:\x01\x30\x12\x0c\n\x01y\x18\x02 \x01(\x01:\x01\x30\"\'\n\x03Map\x12 \n\x04pose\x18\x01 \x03(\x0b\x32\x12.interface.Point2D')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'map_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_POINT2D']._serialized_start=24
  _globals['_POINT2D']._serialized_end=61
  _globals['_MAP']._serialized_start=63
  _globals['_MAP']._serialized_end=102
# @@protoc_insertion_point(module_scope)
