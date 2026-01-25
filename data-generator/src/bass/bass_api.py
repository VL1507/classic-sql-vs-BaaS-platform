import requests


class Back4AppApi:
    def __init__(self, application_id: str, rest_api_key: str) -> None:
        self.headers = {
            "X-Parse-Application-Id": application_id,
            "X-Parse-REST-API-Key": rest_api_key,
            "Content-Type": "application/json",
        }
        self.base_url = "https://parseapi.back4app.com/classes/"

    def create_user_types(self, type_: str) -> str:
        json_data = {"type": type_}
        res = requests.post(
            url=self.base_url + "UserTypes",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_houses(self, address: str) -> str:
        json_data = {"address": address}
        res = requests.post(
            url=self.base_url + "Houses",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_device_types(self, type_: str, name: str) -> str:
        json_data = {"type": type_, "name": name}
        res = requests.post(
            url=self.base_url + "DeviceTypes",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_scenaries(self, time_from: int, time_till: int) -> str:
        json_data = {"time_from": time_from, "time_till": time_till}
        res = requests.post(
            url=self.base_url + "Scenaries",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_device_types_to_user_types(
        self, device_type_id: str, user_type_id: str
    ) -> str:
        json_data = {
            "device_type_id": {
                "__type": "Pointer",
                "className": "DeviceTypes",
                "objectId": device_type_id,
            },
            "user_type_id": {
                "__type": "Pointer",
                "className": "UserTypes",
                "objectId": user_type_id,
            },
        }
        res = requests.post(
            url=self.base_url + "DeviceTypesToUserTypes",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_user(self, name: str, user_type_id: str) -> str:
        json_data = {
            "name": name,
            "user_type_id": {
                "__type": "Pointer",
                "className": "UserTypes",
                "objectId": user_type_id,
            },
        }
        res = requests.post(
            url=self.base_url + "Users",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_devices(self, house_id: str, device_type_id: str) -> str:
        json_data = {
            "house_id": {
                "__type": "Pointer",
                "className": "Houses",
                "objectId": house_id,
            },
            "device_type_id": {
                "__type": "Pointer",
                "className": "DeviceTypes",
                "objectId": device_type_id,
            },
        }
        res = requests.post(
            url=self.base_url + "Devices",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_co_ne_to_devises(
        self, scenary_id: str, device_id: str, is_on: bool
    ) -> str:
        json_data = {
            "scenary_id": {
                "__type": "Pointer",
                "className": "Scenaries",
                "objectId": scenary_id,
            },
            "device_id": {
                "__type": "Pointer",
                "className": "Devices",
                "objectId": device_id,
            },
            "is_on": is_on,
        }
        res = requests.post(
            url=self.base_url + "CoNEToDevises",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_activations_to_devices(
        self, scenary_id: str, device_id: str, is_on: bool, affect_time: int
    ) -> str:
        json_data = {
            "scenary_id": {
                "__type": "Pointer",
                "className": "Scenaries",
                "objectId": scenary_id,
            },
            "device_id": {
                "__type": "Pointer",
                "className": "Devices",
                "objectId": device_id,
            },
            "is_on": is_on,
            "affect_time": affect_time,
        }
        res = requests.post(
            url=self.base_url + "ActivationsToDevices",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_events(
        self,
        user_id: str,
        device_id: str,
        scenary_id: str,
        value: bool,
    ) -> str:
        json_data = {
            "user_id": {
                "__type": "Pointer",
                "className": "Users",
                "objectId": user_id,
            },
            "device_id": {
                "__type": "Pointer",
                "className": "Devices",
                "objectId": device_id,
            },
            "scenary_id": {
                "__type": "Pointer",
                "className": "Scenaries",
                "objectId": scenary_id,
            },
            "value": value,
        }
        res = requests.post(
            url=self.base_url + "Events",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]

    def create_measures(
        self,
        device_id: str,
        measure_time: int,
        value: int,
    ) -> str:
        json_data = {
            "device_id": {
                "__type": "Pointer",
                "className": "Devices",
                "objectId": device_id,
            },
            "measure_time": measure_time,
            "value": value,
        }
        res = requests.post(
            url=self.base_url + "Measures",
            json=json_data,
            headers=self.headers,
            timeout=30,
        )
        return res.json()["objectId"]
