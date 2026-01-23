from dataclasses import dataclass


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

    device_type_id: str
    user_type_id: str


@dataclass
class Devices:
    object_id: str | None

    house_id: str
    device_type_id: str


@dataclass
class Users:
    object_id: str | None

    name: str
    user_type_id: str


@dataclass
class ActivationsToDevices:
    object_id: str | None

    scenario_id: str
    device_id: str
    is_on: bool
    affect_time: int | None


@dataclass
class CoNEToDevices:
    object_id: str | None

    scenario_id: str
    device_id: str
    is_on: bool


@dataclass
class Events:
    object_id: str | None

    value: bool
    user_id: str | None
    device_id: str | None
    scenario_id: str | None


@dataclass
class Measures:
    object_id: str | None

    device_id: str
    measure_time: int
    value: int | None
