import datetime
import decimal
from typing import Optional

from sqlalchemy import (
    DateTime,
    Double,
    ForeignKeyConstraint,
    Index,
    String,
    Time,
)
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DeviceTypes(Base):
    __tablename__ = "DeviceTypes"
    __table_args__ = (Index("type", "type", unique=True),)

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    user_type: Mapped[list["UserTypes"]] = relationship(
        "UserTypes",
        secondary="DeviceTypesToUserTypes",
        back_populates="device_type",
    )
    Devices: Mapped[list["Devices"]] = relationship(
        "Devices", back_populates="device_type"
    )


class Houses(Base):
    __tablename__ = "Houses"

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    Devices: Mapped[list["Devices"]] = relationship(
        "Devices", back_populates="house"
    )


class Scenarios(Base):
    __tablename__ = "Scenarios"

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    time_from: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    time_till: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    ActivationsToDevices: Mapped[list["ActivationsToDevices"]] = relationship(
        "ActivationsToDevices", back_populates="scenario"
    )
    CoNEToDevices: Mapped[list["CoNEToDevices"]] = relationship(
        "CoNEToDevices", back_populates="scenario"
    )
    Events: Mapped[list["Events"]] = relationship(
        "Events", back_populates="scenario"
    )


class UserTypes(Base):
    __tablename__ = "UserTypes"

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)

    device_type: Mapped[list["DeviceTypes"]] = relationship(
        "DeviceTypes",
        secondary="DeviceTypesToUserTypes",
        back_populates="user_type",
    )
    Users: Mapped[list["Users"]] = relationship(
        "Users", back_populates="user_type"
    )


class DeviceTypesToUserTypes(Base):
    __tablename__ = "DeviceTypesToUserTypes"
    __table_args__ = (
        ForeignKeyConstraint(
            ["device_type_id"],
            ["DeviceTypes.id"],
            name="DeviceTypesToUserTypes_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["user_type_id"],
            ["UserTypes.id"],
            name="DeviceTypesToUserTypes_ibfk_1",
        ),
        Index("user_type_id", "user_type_id"),
    )
    device_type_id: int = mapped_column(INTEGER(11), primary_key=True)
    user_type_id: int = mapped_column(INTEGER(11), primary_key=True)


class Devices(Base):
    __tablename__ = "Devices"
    __table_args__ = (
        ForeignKeyConstraint(
            ["device_type_id"], ["DeviceTypes.id"], name="Devices_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["house_id"], ["Houses.id"], name="Devices_ibfk_1"
        ),
        Index("device_type_id", "device_type_id"),
        Index("house_id", "house_id"),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    house_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    device_type_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    device_type: Mapped["DeviceTypes"] = relationship(
        "DeviceTypes", back_populates="Devices"
    )
    house: Mapped["Houses"] = relationship("Houses", back_populates="Devices")
    ActivationsToDevices: Mapped[list["ActivationsToDevices"]] = relationship(
        "ActivationsToDevices", back_populates="device"
    )
    CoNEToDevices: Mapped[list["CoNEToDevices"]] = relationship(
        "CoNEToDevices", back_populates="device"
    )
    Events: Mapped[list["Events"]] = relationship(
        "Events", back_populates="device"
    )
    Measures: Mapped[list["Measures"]] = relationship(
        "Measures", back_populates="device"
    )


class Users(Base):
    __tablename__ = "Users"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_type_id"], ["UserTypes.id"], name="Users_ibfk_1"
        ),
        Index("user_type_id", "user_type_id"),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_type_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    user_type: Mapped["UserTypes"] = relationship(
        "UserTypes", back_populates="Users"
    )
    Events: Mapped[list["Events"]] = relationship(
        "Events", back_populates="user"
    )


class ActivationsToDevices(Base):
    __tablename__ = "ActivationsToDevices"
    __table_args__ = (
        ForeignKeyConstraint(
            ["device_id"], ["Devices.id"], name="ActivationsToDevices_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["scenario_id"],
            ["Scenarios.id"],
            name="ActivationsToDevices_ibfk_1",
        ),
        Index("device_id", "device_id"),
    )

    scenario_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    device_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    is_on: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    affect_time: Mapped[datetime.time | None] = mapped_column(Time)

    device: Mapped["Devices"] = relationship(
        "Devices", back_populates="ActivationsToDevices"
    )
    scenario: Mapped["Scenarios"] = relationship(
        "Scenarios", back_populates="ActivationsToDevices"
    )


class CoNEToDevices(Base):
    __tablename__ = "CoNEToDevices"
    __table_args__ = (
        ForeignKeyConstraint(
            ["device_id"], ["Devices.id"], name="CoNEToDevices_ibfk_1"
        ),
        ForeignKeyConstraint(
            ["scenario_id"], ["Scenarios.id"], name="CoNEToDevices_ibfk_2"
        ),
        Index("device_id", "device_id"),
        {"comment": "Conjunction of necessary events to devices"},
    )

    scenario_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    device_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    is_on: Mapped[int] = mapped_column(TINYINT(1), nullable=False)

    device: Mapped["Devices"] = relationship(
        "Devices", back_populates="CoNEToDevices"
    )
    scenario: Mapped["Scenarios"] = relationship(
        "Scenarios", back_populates="CoNEToDevices"
    )


class Events(Base):
    __tablename__ = "Events"
    __table_args__ = (
        ForeignKeyConstraint(
            ["device_id"], ["Devices.id"], name="Events_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["scenario_id"], ["Scenarios.id"], name="Events_ibfk_3"
        ),
        ForeignKeyConstraint(["user_id"], ["Users.id"], name="Events_ibfk_1"),
        Index("device_id", "device_id"),
        Index("scenario_id", "scenario_id"),
        Index("user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    value: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int | None] = mapped_column(INTEGER(11))
    device_id: Mapped[int | None] = mapped_column(INTEGER(11))
    scenario_id: Mapped[int | None] = mapped_column(INTEGER(11))

    device: Mapped[Optional["Devices"]] = relationship(
        "Devices", back_populates="Events"
    )
    scenario: Mapped[Optional["Scenarios"]] = relationship(
        "Scenarios", back_populates="Events"
    )
    user: Mapped[Optional["Users"]] = relationship(
        "Users", back_populates="Events"
    )


class Measures(Base):
    __tablename__ = "Measures"
    __table_args__ = (
        ForeignKeyConstraint(
            ["device_id"], ["Devices.id"], name="Measures_ibfk_1"
        ),
        Index("device_id", "device_id"),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    device_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    measure_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False
    )
    value: Mapped[decimal.Decimal | None] = mapped_column(
        Double(asdecimal=True)
    )

    device: Mapped["Devices"] = relationship(
        "Devices", back_populates="Measures"
    )
