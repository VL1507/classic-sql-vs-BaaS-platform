from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class UserDeviceTypes:
    user_name: str
    user_type: str
    device_type: str
    device_name: str


def find_user_device_types(
    session: Session, user_name: str
) -> list[UserDeviceTypes]:
    stmt = text("""SELECT u.name,
    ut.type,
    dt.type,
    dt.name
FROM DeviceTypesToUserTypes dttut
    LEFT JOIN DeviceTypes dt ON dt.id = dttut.device_type_id
    LEFT JOIN UserTypes ut ON ut.id = dttut.user_type_id
    LEFT JOIN Users u ON u.user_type_id = ut.id
    AND u.name = :user_name
WHERE u.id IS NOT Null;""")

    res = session.execute(stmt, {"user_name": user_name})

    return [
        UserDeviceTypes(
            user_name=utd[0],
            user_type=utd[1],
            device_type=utd[2],
            device_name=utd[3],
        )
        for utd in res
    ]


@dataclass
class HousesWithActivatedDevices:
    id: int
    address: str


def get_houses_with_activated_devices(
    session: Session,
) -> list[HousesWithActivatedDevices]:
    stmt = text("""SELECT DISTINCT h.id,
    h.address
FROM Houses h
    INNER JOIN Devices d ON h.id = d.house_id
    INNER JOIN ActivationsToDevices atd ON d.id = atd.device_id;""")

    res = session.execute(stmt)

    return [
        HousesWithActivatedDevices(id=house[0], address=house[1])
        for house in res
    ]


@dataclass
class MaxThermostatValue:
    address: str
    measure_time: datetime
    value: float


def get_max_thermostat_value(session: Session) -> MaxThermostatValue:
    stmt = text("""SELECT h.address,
    m.measure_time,
    m.value
FROM Measures m
    LEFT JOIN Devices d ON m.device_id = d.id
    LEFT JOIN DeviceTypes dt ON d.device_type_id = dt.id
    LEFT JOIN Houses h ON h.id = d.house_id
WHERE dt.type = 'thermostat'
ORDER BY m.value DESC
LIMIT 1;""")

    res = session.execute(stmt).first()

    return MaxThermostatValue(
        address=res[0],
        measure_time=res[1],
        value=res[2],
    )


def start_req_db(session: Session) -> None:
    func = input(
        """Выберите функцию:
        - findUserDeviceTypes, 
        - getHousesWithActivatedDevices
        - getMaxThermostatValue
        : """
    )
    if func == "findUserDeviceTypes":
        user_name = input("Введите имя: ")
        print(find_user_device_types(session=session, user_name=user_name))
    elif func == "getHousesWithActivatedDevices":
        print(get_houses_with_activated_devices(session=session))
    elif func == "getMaxThermostatValue":
        print(get_max_thermostat_value(session=session))
    else:
        print("Неверное имя функции")
