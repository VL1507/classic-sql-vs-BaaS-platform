from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass
class UserDeviceTypes:
    user_name: str
    user_type: str
    device_type: str
    device_name: str


def find_user_device_types(
    application_id: str, rest_api_key: str, user_name: str
) -> list[UserDeviceTypes]:
    headers = {
        "X-Parse-Application-Id": application_id,
        "X-Parse-REST-API-Key": rest_api_key,
        "Content-Type": "application/json",
    }
    url = "https://parseapi.back4app.com/functions/findUserDeviceTypes"

    res = requests.post(
        url=url,
        json={"name": user_name},
        headers=headers,
        timeout=30,
    )

    if res.status_code != 200:
        raise Exception

    result = res.json()["result"]

    return [
        UserDeviceTypes(
            user_name=utd["userName"],
            user_type=utd["userType"],
            device_type=utd["deviceType"],
            device_name=utd["deviceName"],
        )
        for utd in result
    ]


@dataclass
class HousesWithActivatedDevices:
    objectId: str
    address: str


def get_houses_with_activated_devices(
    application_id: str,
    rest_api_key: str,
) -> list[HousesWithActivatedDevices]:
    headers = {
        "X-Parse-Application-Id": application_id,
        "X-Parse-REST-API-Key": rest_api_key,
        "Content-Type": "application/json",
    }

    url = (
        "https://parseapi.back4app.com/functions/getHousesWithActivatedDevices"
    )

    res = requests.post(
        url=url,
        headers=headers,
        timeout=30,
    )

    if res.status_code != 200:
        raise Exception

    houses = res.json()["result"]["houses"]

    return [
        HousesWithActivatedDevices(
            objectId=house["objectId"], address=house["address"]
        )
        for house in houses
    ]


@dataclass
class MaxThermostatValue:
    address: str
    measure_time: int
    value: float


def get_max_thermostat_value(
    application_id: str, rest_api_key: str
) -> MaxThermostatValue:
    headers = {
        "X-Parse-Application-Id": application_id,
        "X-Parse-REST-API-Key": rest_api_key,
        "Content-Type": "application/json",
    }

    url = "https://parseapi.back4app.com/functions/getMaxThermostatValue"

    res = requests.post(
        url=url,
        headers=headers,
        timeout=30,
    )

    if res.status_code != 200:
        raise Exception

    result = res.json()["result"]

    return MaxThermostatValue(
        address=result["address"],
        measure_time=result["measure_time"],
        value=result["value"],
    )


def start_req_back4app(application_id: str, rest_api_key: str) -> None:
    func = input(
        """Выберите функцию:
        - findUserDeviceTypes, 
        - getHousesWithActivatedDevices
        - getMaxThermostatValue
        : """
    )
    if func == "findUserDeviceTypes":
        user_name = input("Введите имя: ")
        print(
            find_user_device_types(
                application_id=application_id,
                rest_api_key=rest_api_key,
                user_name=user_name,
            )
        )
    elif func == "getHousesWithActivatedDevices":
        print(
            get_houses_with_activated_devices(
                application_id=application_id, rest_api_key=rest_api_key
            )
        )
    elif func == "getMaxThermostatValue":
        print(
            get_max_thermostat_value(
                application_id=application_id, rest_api_key=rest_api_key
            )
        )
    else:
        print("Неверное имя функции")
