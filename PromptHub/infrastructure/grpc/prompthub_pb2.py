# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: prompthub.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'prompthub.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fprompthub.proto\x12\tprompthub\".\n\rPromptMessage\x12\x0c\n\x04Role\x18\x01 \x01(\t\x12\x0f\n\x07\x43ontent\x18\x02 \x01(\t\"\x1c\n\x0bInfoMessage\x12\r\n\x05State\x18\x01 \x01(\t\"\xa9\x01\n\x17PromptProcessingRequest\x12\x0c\n\x04Mode\x18\x01 \x01(\t\x12\r\n\x05Title\x18\x02 \x01(\t\x12(\n\x06Prompt\x18\x03 \x03(\x0b\x32\x18.prompthub.PromptMessage\x12\r\n\x05Model\x18\x04 \x01(\t\x12\x10\n\x08Provider\x18\x05 \x01(\t\x12\x11\n\tMaxTokens\x18\x06 \x01(\x05\x12\x13\n\x0bTemperature\x18\x07 \x01(\x02\"\xba\x01\n\x18PromptProcessingResponse\x12(\n\x06Result\x18\x01 \x01(\x0b\x32\x18.prompthub.PromptMessage\x12+\n\x0bInformation\x18\x02 \x01(\x0b\x32\x16.prompthub.InfoMessage\x12\r\n\x05Model\x18\x03 \x01(\t\x12\x10\n\x08Provider\x18\x04 \x01(\t\x12\x11\n\tMaxTokens\x18\x05 \x01(\x05\x12\x13\n\x0bTemperature\x18\x06 \x01(\x02\x32h\n\tPromptHub\x12[\n\x10PromptProcessing\x12\".prompthub.PromptProcessingRequest\x1a#.prompthub.PromptProcessingResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'prompthub_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PROMPTMESSAGE']._serialized_start=30
  _globals['_PROMPTMESSAGE']._serialized_end=76
  _globals['_INFOMESSAGE']._serialized_start=78
  _globals['_INFOMESSAGE']._serialized_end=106
  _globals['_PROMPTPROCESSINGREQUEST']._serialized_start=109
  _globals['_PROMPTPROCESSINGREQUEST']._serialized_end=278
  _globals['_PROMPTPROCESSINGRESPONSE']._serialized_start=281
  _globals['_PROMPTPROCESSINGRESPONSE']._serialized_end=467
  _globals['_PROMPTHUB']._serialized_start=469
  _globals['_PROMPTHUB']._serialized_end=573
# @@protoc_insertion_point(module_scope)
