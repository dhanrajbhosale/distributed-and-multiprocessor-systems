from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BranchRequest(_message.Message):
    __slots__ = ["interface", "id", "money", "clock", "type", "branch_id"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    interface: str
    id: int
    money: int
    clock: int
    type: str
    branch_id: int
    def __init__(self, interface: _Optional[str] = ..., id: _Optional[int] = ..., money: _Optional[int] = ..., clock: _Optional[int] = ..., type: _Optional[str] = ..., branch_id: _Optional[int] = ...) -> None: ...

class BranchResponse(_message.Message):
    __slots__ = ["interface", "result", "balance", "id", "clock", "eventid"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    interface: str
    result: str
    balance: int
    id: int
    clock: int
    eventid: int
    def __init__(self, interface: _Optional[str] = ..., result: _Optional[str] = ..., balance: _Optional[int] = ..., id: _Optional[int] = ..., clock: _Optional[int] = ..., eventid: _Optional[int] = ...) -> None: ...
