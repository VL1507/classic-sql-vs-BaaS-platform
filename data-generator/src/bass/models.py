import datetime
import decimal
from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceTypes:
    object_id: str | None

    type: str
    name: str


@dataclass
class Houses:
    object_id: str | None

    address: str


@dataclass
class Scenarios:
    object_id: str | None

    time_from: int
    time_till: int


@dataclass
class UserTypes:
    object_id: str | None

    type: str


@dataclass
class DeviceTypesToUserTypes:
    object_id: str | None

    device_type_id: int
    user_type_id: int


@dataclass
class Devices:
    object_id: str | None

    house_id: int
    device_type_id: int


@dataclass
class Users:
    object_id: str | None

    name: str
    user_type_id: int


@dataclass
class ActivationsToDevices:
    scenario_id: int
    device_id: int
    is_on: bool
    affect_time: datetime.time | None


@dataclass
class CoNEToDevices:
    scenario_id: int
    device_id: int
    is_on: bool


@dataclass
class Events:
    object_id: str | None

    value: bool
    user_id: int | None
    device_id: int | None
    scenario_id: int | None


@dataclass
class Measures:
    object_id: str | None

    device_id: int
    measure_time: datetime.datetime
    value: decimal.Decimal | None
