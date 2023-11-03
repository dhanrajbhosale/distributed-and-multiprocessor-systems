from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BranchRequest(_message.Message):
    __slots__ = ["interface", "id", "money"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    interface: str
    id: int
    money: int
    def __init__(self, interface: _Optional[str] = ..., id: _Optional[int] = ..., money: _Optional[int] = ...) -> None: ...

class BranchResponse(_message.Message):
    __slots__ = ["interface", "result", "balance"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    interface: str
    result: str
    balance: int
    def __init__(self, interface: _Optional[str] = ..., result: _Optional[str] = ..., balance: _Optional[int] = ...) -> None: ...
