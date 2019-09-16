# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: recoverykit.proto

# flake8: noqa

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="recoverykit.proto",
    package="co.upvest.recoverykit",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x11recoverykit.proto\x12\x15\x63o.upvest.recoverykit"E\n\x0c\x43ipherParams\x12\x13\n\x0b\x65phemeralpk\x18\x01 \x01(\x0c\x12\r\n\x05nonce\x18\x02 \x01(\x0c\x12\x11\n\trecipient\x18\x03 \x01(\x0c"S\n\nHashParams\x12\x0b\n\x03len\x18\x01 \x01(\r\x12\t\n\x01m\x18\x02 \x01(\r\x12\t\n\x01p\x18\x03 \x01(\r\x12\x0c\n\x04salt\x18\x04 \x01(\x0c\x12\t\n\x01t\x18\x05 \x01(\r\x12\t\n\x01v\x18\x06 \x01(\r"\xc0\x01\n\x04Seed\x12\x0e\n\x06\x63ipher\x18\x01 \x01(\t\x12\x39\n\x0c\x63ipherparams\x18\x02 \x01(\x0b\x32#.co.upvest.recoverykit.CipherParams\x12\x12\n\nciphertext\x18\x03 \x01(\x0c\x12\x0c\n\x04hash\x18\x04 \x01(\x0c\x12\x14\n\x0chashfunction\x18\x05 \x01(\t\x12\x35\n\nhashparams\x18\x06 \x01(\x0b\x32!.co.upvest.recoverykit.HashParams"\xb7\x01\n\x0bRecoveryKit\x12)\n\x04seed\x18\x01 \x01(\x0b\x32\x1b.co.upvest.recoverykit.Seed\x12\x10\n\x08seedhash\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x10\n\x08\x64\x61tetime\x18\x04 \x01(\x03\x12\x11\n\tclient_ip\x18\x05 \x01(\t\x12\x0f\n\x07version\x18\x06 \x01(\t\x12\x12\n\nuser_agent\x18\x07 \x01(\t\x12\x0f\n\x07user_id\x18\x08 \x01(\rb\x06proto3'
    ),
)


_CIPHERPARAMS = _descriptor.Descriptor(
    name="CipherParams",
    full_name="co.upvest.recoverykit.CipherParams",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="ephemeralpk",
            full_name="co.upvest.recoverykit.CipherParams.ephemeralpk",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="nonce",
            full_name="co.upvest.recoverykit.CipherParams.nonce",
            index=1,
            number=2,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="recipient",
            full_name="co.upvest.recoverykit.CipherParams.recipient",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=44,
    serialized_end=113,
)


_HASHPARAMS = _descriptor.Descriptor(
    name="HashParams",
    full_name="co.upvest.recoverykit.HashParams",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="len",
            full_name="co.upvest.recoverykit.HashParams.len",
            index=0,
            number=1,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="m",
            full_name="co.upvest.recoverykit.HashParams.m",
            index=1,
            number=2,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="p",
            full_name="co.upvest.recoverykit.HashParams.p",
            index=2,
            number=3,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="salt",
            full_name="co.upvest.recoverykit.HashParams.salt",
            index=3,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="t",
            full_name="co.upvest.recoverykit.HashParams.t",
            index=4,
            number=5,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="v",
            full_name="co.upvest.recoverykit.HashParams.v",
            index=5,
            number=6,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=115,
    serialized_end=198,
)


_SEED = _descriptor.Descriptor(
    name="Seed",
    full_name="co.upvest.recoverykit.Seed",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="cipher",
            full_name="co.upvest.recoverykit.Seed.cipher",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="cipherparams",
            full_name="co.upvest.recoverykit.Seed.cipherparams",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="ciphertext",
            full_name="co.upvest.recoverykit.Seed.ciphertext",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="hash",
            full_name="co.upvest.recoverykit.Seed.hash",
            index=3,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="hashfunction",
            full_name="co.upvest.recoverykit.Seed.hashfunction",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="hashparams",
            full_name="co.upvest.recoverykit.Seed.hashparams",
            index=5,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=201,
    serialized_end=393,
)


_RECOVERYKIT = _descriptor.Descriptor(
    name="RecoveryKit",
    full_name="co.upvest.recoverykit.RecoveryKit",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="seed",
            full_name="co.upvest.recoverykit.RecoveryKit.seed",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="seedhash",
            full_name="co.upvest.recoverykit.RecoveryKit.seedhash",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="username",
            full_name="co.upvest.recoverykit.RecoveryKit.username",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="datetime",
            full_name="co.upvest.recoverykit.RecoveryKit.datetime",
            index=3,
            number=4,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="client_ip",
            full_name="co.upvest.recoverykit.RecoveryKit.client_ip",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="version",
            full_name="co.upvest.recoverykit.RecoveryKit.version",
            index=5,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="user_agent",
            full_name="co.upvest.recoverykit.RecoveryKit.user_agent",
            index=6,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="user_id",
            full_name="co.upvest.recoverykit.RecoveryKit.user_id",
            index=7,
            number=8,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=396,
    serialized_end=579,
)

_SEED.fields_by_name["cipherparams"].message_type = _CIPHERPARAMS
_SEED.fields_by_name["hashparams"].message_type = _HASHPARAMS
_RECOVERYKIT.fields_by_name["seed"].message_type = _SEED
DESCRIPTOR.message_types_by_name["CipherParams"] = _CIPHERPARAMS
DESCRIPTOR.message_types_by_name["HashParams"] = _HASHPARAMS
DESCRIPTOR.message_types_by_name["Seed"] = _SEED
DESCRIPTOR.message_types_by_name["RecoveryKit"] = _RECOVERYKIT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CipherParams = _reflection.GeneratedProtocolMessageType(
    "CipherParams",
    (_message.Message,),
    {
        "DESCRIPTOR": _CIPHERPARAMS,
        "__module__": "recoverykit_pb2"
        # @@protoc_insertion_point(class_scope:co.upvest.recoverykit.CipherParams)
    },
)
_sym_db.RegisterMessage(CipherParams)

HashParams = _reflection.GeneratedProtocolMessageType(
    "HashParams",
    (_message.Message,),
    {
        "DESCRIPTOR": _HASHPARAMS,
        "__module__": "recoverykit_pb2"
        # @@protoc_insertion_point(class_scope:co.upvest.recoverykit.HashParams)
    },
)
_sym_db.RegisterMessage(HashParams)

Seed = _reflection.GeneratedProtocolMessageType(
    "Seed",
    (_message.Message,),
    {
        "DESCRIPTOR": _SEED,
        "__module__": "recoverykit_pb2"
        # @@protoc_insertion_point(class_scope:co.upvest.recoverykit.Seed)
    },
)
_sym_db.RegisterMessage(Seed)

RecoveryKit = _reflection.GeneratedProtocolMessageType(
    "RecoveryKit",
    (_message.Message,),
    {
        "DESCRIPTOR": _RECOVERYKIT,
        "__module__": "recoverykit_pb2"
        # @@protoc_insertion_point(class_scope:co.upvest.recoverykit.RecoveryKit)
    },
)
_sym_db.RegisterMessage(RecoveryKit)


# @@protoc_insertion_point(module_scope)