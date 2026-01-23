from dataclasses import dataclass
from datetime import datetime


@dataclass
class DBSchema:
    # DeviceTypes
    device_types_type: str
    device_types_name: str

    # Houses
    houses_address: str

    # Scenarios
    scenarios_time_from: datetime.time
    scenarios_time_till: datetime.time

    # UserTypes
    user_types_type: str

    # Users
    user_name: str
