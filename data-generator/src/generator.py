import random
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from logging import getLogger

from faker import Faker
from sqlalchemy.orm import Session
from tqdm import tqdm

from models import (
    ActivationsToDevices,
    Base,
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


# Faker(42)

fake = Faker("ru_RU")


def generate_time_between(hour_start: int, hour_end: int) -> time:
    """Случайное время в диапазоне часов"""
    hour = random.randint(hour_start, hour_end)
    minute = random.randint(0, 59)
    return time(hour, minute)


def create_reference_data(
    session: Session,
) -> tuple[list[UserTypes], list[DeviceTypes]]:
    """Создаём справочники — их обычно немного и они стабильны"""

    user_types_data = [
        {"type": "Взрослый"},
        {"type": "Ребёнок"},
        {"type": "Гость"},
        {"type": "Пенсионер"},
    ]
    user_types = [UserTypes(**d) for d in user_types_data]
    session.add_all(user_types)
    session.flush()

    device_types_data = [
        {"type": "light", "name": "Умная лампа"},
        {"type": "socket", "name": "Умная розетка"},
        {"type": "thermostat", "name": "Термостат"},
        {"type": "motion", "name": "Датчик движения"},
        {"type": "door", "name": "Датчик открытия двери"},
        {"type": "camera", "name": "Камера"},
    ]
    device_types = [DeviceTypes(**d) for d in device_types_data]
    session.add_all(device_types)
    session.flush()

    associations = []
    for dt in device_types:
        allowed_user_types = random.sample(
            user_types, k=random.randint(1, len(user_types))
        )
        associations.extend(
            DeviceTypesToUserTypes(device_type_id=dt.id, user_type_id=ut.id)
            for ut in allowed_user_types
        )
    session.add_all(associations)
    session.flush()

    return user_types, device_types


def create_houses_and_devices(
    session: Session,
    device_types: list[DeviceTypes],
    count_houses: int = 5,
    devices_per_house: int = 6,
) -> tuple[list[Houses], list[Devices]]:
    houses: list[Houses] = []
    all_devices: list[Devices] = []

    for _ in tqdm(range(count_houses), desc="create_houses_and_devices"):
        house = Houses(address=fake.address().replace("\n", ", "))
        houses.append(house)
        session.add(house)
        session.flush()

        for dt in random.sample(
            device_types, k=min(devices_per_house, len(device_types))
        ):
            device = Devices(house_id=house.id, device_type_id=dt.id)
            all_devices.append(device)
            session.add(device)

    session.flush()
    return houses, all_devices


def create_users(
    session: Session, user_types: list[UserTypes], count_users: int = 12
) -> list[Users]:
    users: list[Users] = []
    for _ in tqdm(
        range(count_users),
        desc="create_users",
    ):
        ut = random.choice(user_types)
        user = Users(name=fake.name(), user_type_id=ut.id)
        users.append(user)
        session.add(user)
    session.flush()
    return users


def create_scenarios(
    session: Session, count_scenarios: int = 8
) -> list[Scenarios]:
    scenarios: list[Scenarios] = []
    for _ in tqdm(range(count_scenarios), desc="create_scenarios"):
        t_from = generate_time_between(6, 22)
        t_till = (
            generate_time_between(t_from.hour + 1, 23)
            if t_from.hour < 22
            else time(23, 59)
        )

        sc = Scenarios(time_from=t_from, time_till=t_till)
        scenarios.append(sc)
        session.add(sc)
    session.flush()
    return scenarios


def create_activations_and_cone(
    session: Session, devices: list[Devices], scenarios: list[Scenarios]
) -> None:
    activations = []
    cones = []

    for scenario in tqdm(scenarios, desc="create_activations_and_cone"):
        selected_devices = random.sample(
            devices, k=random.randint(2, min(6, len(devices)))
        )

        for dev in selected_devices:
            if random.random() < 0.75:  # ~75% устройств активируются
                activations.append(
                    ActivationsToDevices(
                        scenario_id=scenario.id,
                        device_id=dev.id,
                        is_on=random.choice([0, 1]),
                        affect_time=generate_time_between(0, 23)
                        if random.random() < 0.4
                        else None,
                    )
                )

            if random.random() < 0.35:
                cones.append(
                    CoNEToDevices(
                        scenario_id=scenario.id,
                        device_id=dev.id,
                        is_on=random.choice([0, 1]),
                    )
                )

    session.add_all(activations)
    session.add_all(cones)
    session.flush()


def create_events_and_measures(
    session: Session,
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
            value=random.choice([0, 1]),
            user_id=random.choice([None, random.choice(users).id]),
            device_id=random.choice([None, random.choice(devices).id]),
            scenario_id=random.choice([None, random.choice(scenarios).id]),
        )
        events.append(ev)

    for _ in tqdm(
        range(count_measures),
        desc="create_measures",
    ):
        past = now - timedelta(
            days=random.randint(0, 60), hours=random.randint(0, 23)
        )
        meas = Measures(
            device_id=random.choice(devices).id,
            measure_time=past,
            value=Decimal(random.uniform(0.0, 100.0)).quantize(
                Decimal("0.01")
            ),
        )
        measures.append(meas)

    session.add_all(events)
    session.add_all(measures)


def populate_database(session: Session, *, clear_first: bool = True) -> None:
    """
    Основная функция - запуск всего генератора
    """
    if clear_first:
        for table in tqdm(
            reversed(Base.metadata.sorted_tables), desc="table.delete"
        ):
            session.execute(table.delete())

    user_types, device_types = create_reference_data(session)
    houses, devices = create_houses_and_devices(
        session, device_types, count_houses=200
    )
    users = create_users(session, user_types, count_users=200)
    scenarios = create_scenarios(session, count_scenarios=50)

    create_activations_and_cone(session, devices, scenarios)
    create_events_and_measures(session, users, devices, scenarios)

    session.commit()
    log = (
        f"Сгенерировано:\n"
        f"  домов       : {len(houses)}\n"
        f"  устройств    : {len(devices)}\n"
        f"  пользователей: {len(users)}\n"
        f"  сценариев    : {len(scenarios)}"
    )
    logger.info(log)
