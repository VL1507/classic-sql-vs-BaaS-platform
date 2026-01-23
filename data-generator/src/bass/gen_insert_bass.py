import random
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from logging import getLogger

from faker import Faker
from tqdm import tqdm

from bass.bass_api import Back4AppApi
from bass.models import (
    ActivationsToDevices,
    CoNEToDevices,
    Devices,
    DeviceTypes,
    DeviceTypesToUserTypes,
    Events,
    Houses,
    Measures,
    Scenarios,
    Users,
    UserTypes,
)

logger = getLogger(name=__name__)

random.seed(42)

Faker.seed(42)

fake = Faker("ru_RU")


def generate_time_between(hour_start: int, hour_end: int) -> time:
    """Случайное время в диапазоне часов"""
    hour = random.randint(hour_start, hour_end)
    minute = random.randint(0, 59)
    return time(hour, minute)


def time_to_int(t: time) -> int:
    return 60 * t.hour + t.minute


def create_reference_data(
    back4app_api: Back4AppApi,
) -> tuple[list[UserTypes], list[DeviceTypes]]:
    """Создаём справочники — их обычно немного и они стабильны"""

    user_types_data = [
        {"type": "Взрослый"},
        {"type": "Ребёнок"},
        {"type": "Гость"},
        {"type": "Пенсионер"},
    ]

    user_types: list[UserTypes] = []
    for user_type in user_types_data:
        ut = UserTypes(object_id=None, type=user_type["type"])
        object_id = back4app_api.create_user_types(type_=ut.type)
        ut.object_id = object_id
        user_types.append(ut)

    device_types_data = [
        {"type": "light", "name": "Умная лампа"},
        {"type": "socket", "name": "Умная розетка"},
        {"type": "thermostat", "name": "Термостат"},
        {"type": "motion", "name": "Датчик движения"},
        {"type": "door", "name": "Датчик открытия двери"},
        {"type": "camera", "name": "Камера"},
    ]

    device_types: list[DeviceTypes] = []
    for device_type in device_types_data:
        dt = DeviceTypes(
            object_id=None, type=device_type["type"], name=device_type["name"]
        )
        object_id = back4app_api.create_device_types(
            type_=dt.type, name=dt.name
        )
        dt.object_id = object_id
        device_types.append(dt)

    associations: list[DeviceTypesToUserTypes] = []
    for dt in tqdm(device_types, desc="device_types"):
        allowed_user_types = random.sample(
            user_types, k=random.randint(1, len(user_types))
        )
        associations.extend(
            DeviceTypesToUserTypes(
                object_id=None,
                device_type_id=dt.object_id,
                user_type_id=ut.object_id,
            )
            for ut in allowed_user_types
        )

    for association in associations:
        object_id = back4app_api.create_device_types_to_user_types(
            device_type_id=association.device_type_id,
            user_type_id=association.user_type_id,
        )
        association.object_id = object_id

    return user_types, device_types


def create_houses_and_devices(
    back4app_api: Back4AppApi,
    device_types: list[DeviceTypes],
    count_houses: int = 5,
    devices_per_house: int = 6,
) -> tuple[list[Houses], list[Devices]]:
    houses: list[Houses] = []
    all_devices: list[Devices] = []

    for _ in tqdm(range(count_houses), desc="create_houses_and_devices"):
        house = Houses(object_id=None, address=fake.address())
        object_id = back4app_api.create_houses(address=house.address)
        house.object_id = object_id
        houses.append(house)

        for dt in random.sample(
            device_types, k=min(devices_per_house, len(device_types))
        ):
            device = Devices(
                object_id=None,
                house_id=house.object_id,
                device_type_id=dt.object_id,
            )
            object_id = back4app_api.create_devices(
                house_id=device.house_id, devise_type_id=device.device_type_id
            )
            device.object_id = object_id
            all_devices.append(device)

    return houses, all_devices


def create_users(
    back4app_api: Back4AppApi,
    user_types: list[UserTypes],
    count_users: int = 12,
) -> list[Users]:
    users: list[Users] = []
    for _ in tqdm(
        range(count_users),
        desc="create_users",
    ):
        ut = random.choice(user_types)
        user = Users(
            object_id=None, name=fake.name(), user_type_id=ut.object_id
        )
        object_id = back4app_api.create_user(
            name=user.name, user_type_id=user.user_type_id
        )
        user.object_id = object_id
        users.append(user)
    return users


def create_scenarios(
    back4app_api: Back4AppApi, count_scenarios: int = 8
) -> list[Scenarios]:
    scenarios: list[Scenarios] = []
    for _ in tqdm(range(count_scenarios), desc="create_scenarios"):
        t_from = generate_time_between(6, 22)
        t_till = (
            generate_time_between(t_from.hour + 1, 23)
            if t_from.hour < 22
            else time(23, 59)
        )

        sc = Scenarios(
            object_id=None,
            time_from=time_to_int(t_from),
            time_till=time_to_int(t_till),
        )
        object_id = back4app_api.create_scenaries(
            time_from=sc.time_from, time_till=sc.time_till
        )
        sc.object_id = object_id
        scenarios.append(sc)
    return scenarios


def create_activations_and_cone(
    back4app_api: Back4AppApi,
    devices: list[Devices],
    scenarios: list[Scenarios],
) -> None:
    activations = []
    cones = []

    for scenario in tqdm(scenarios, desc="create_activations_and_cone"):
        selected_devices = random.sample(
            devices, k=random.randint(2, min(6, len(devices)))
        )

        for dev in selected_devices:
            if random.random() < 0.75:  # ~75% устройств активируются
                activation = ActivationsToDevices(
                    object_id=None,
                    scenario_id=scenario.object_id,
                    device_id=dev.object_id,
                    is_on=bool(random.choice([0, 1])),
                    affect_time=time_to_int(generate_time_between(0, 23))
                    if random.random() < 0.4
                    else None,
                )
                object_id = back4app_api.create_activations_to_devices(
                    scenary_id=activation.scenario_id,
                    device_id=activation.device_id,
                    is_on=activation.is_on,
                    affect_time=activation.affect_time,
                )
                activation.object_id = object_id
                activations.append(activation)

            if random.random() < 0.35:
                cone = CoNEToDevices(
                    object_id=None,
                    scenario_id=scenario.object_id,
                    device_id=dev.object_id,
                    is_on=bool(random.choice([0, 1])),
                )
                object_id = back4app_api.create_co_ne_to_devises(
                    scenary_id=cone.scenario_id,
                    device_id=cone.device_id,
                    is_on=cone.is_on,
                )
                cone.object_id = object_id
                cones.append(cone)


def create_events_and_measures(
    back4app_api: Back4AppApi,
    users: list[Users],
    devices: list[Devices],
    scenarios: list[Scenarios],
    count_events: int = 150,
    count_measures: int = 400,
) -> None:
    events = []
    measures = []

    now = datetime.now(UTC)

    for _ in tqdm(
        range(count_events),
        desc="create_events",
    ):
        ev = Events(
            object_id=None,
            value=bool(random.choice([0, 1])),
            user_id=random.choice([None, random.choice(users).object_id]),
            device_id=random.choice([None, random.choice(devices).object_id]),
            scenario_id=random.choice(
                [None, random.choice(scenarios).object_id]
            ),
        )
        object_id = back4app_api.create_events(
            user_id=ev.user_id,
            device_id=ev.device_id,
            scenary_id=ev.scenario_id,
            value=ev.value,
        )
        ev.object_id = object_id
        events.append(ev)

    for _ in tqdm(
        range(count_measures),
        desc="create_measures",
    ):
        past = now - timedelta(
            days=random.randint(0, 60), hours=random.randint(0, 23)
        )
        meas = Measures(
            object_id=None,
            device_id=random.choice(devices).object_id,
            measure_time=int(past.timestamp()),
            value=int(random.uniform(0.0, 100.0)),
        )
        object_id = back4app_api.create_measures(
            device_id=meas.device_id,
            measure_time=meas.measure_time,
            value=meas.value,
        )
        meas.object_id = object_id
        measures.append(meas)


def populate_bass(
    back4app_api: Back4AppApi, *, clear_first: bool = True
) -> None:
    """
    Основная функция - запуск всего генератора
    """
    # if clear_first:
    #     for table in tqdm(
    #         reversed(Base.metadata.sorted_tables), desc="table.delete"
    #     ):
    #         session.execute(table.delete())

    user_types, device_types = create_reference_data(back4app_api)
    houses, devices = create_houses_and_devices(
        back4app_api, device_types, count_houses=200
    )
    users = create_users(back4app_api, user_types, count_users=200)
    scenarios = create_scenarios(back4app_api, count_scenarios=50)

    create_activations_and_cone(back4app_api, devices, scenarios)
    create_events_and_measures(back4app_api, users, devices, scenarios)

    # session.commit()
    log = (
        f"Сгенерировано:\n"
        f"  домов       : {len(houses)}\n"
        f"  устройств    : {len(devices)}\n"
        f"  пользователей: {len(users)}\n"
        f"  сценариев    : {len(scenarios)}"
    )
    logger.info(log)
