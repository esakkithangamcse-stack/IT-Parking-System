"""Vehicle hierarchy demonstrating abstraction, inheritance, and polymorphism."""

from __future__ import annotations

from abc import ABC, abstractmethod

from parking_system.enums import OwnerType, SlotType, VehicleType


class Vehicle(ABC):
    """Abstract base class for all vehicles entering the IT park."""

    def __init__(
        self,
        vehicle_number: str,
        owner_name: str,
        owner_type: OwnerType,
        vehicle_type: VehicleType,
        is_electric: bool = False,
    ) -> None:
        self._vehicle_number = vehicle_number.strip().upper()
        self._owner_name = owner_name.strip()
        self._owner_type = owner_type
        self._vehicle_type = vehicle_type
        self._is_electric = is_electric

    @property
    def vehicle_number(self) -> str:
        return self._vehicle_number

    @property
    def owner_name(self) -> str:
        return self._owner_name

    @property
    def owner_type(self) -> OwnerType:
        return self._owner_type

    @property
    def vehicle_type(self) -> VehicleType:
        return self._vehicle_type

    @property
    def is_electric(self) -> bool:
        return self._is_electric

    @property
    @abstractmethod
    def wheel_count(self) -> int:
        """Return the number of wheels for this vehicle category."""

    @property
    @abstractmethod
    def hourly_rate(self) -> float:
        """Return the base hourly parking rate."""

    @property
    @abstractmethod
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        """Return slot types that can safely hold this vehicle."""

    def calculate_base_fee(self, chargeable_hours: int) -> float:
        """Polymorphic fee hook; subclasses provide their own hourly rate."""
        return self.hourly_rate * chargeable_hours

    def to_summary(self) -> str:
        return (
            f"{self.vehicle_number} | {self.vehicle_type.value} | "
            f"{self.owner_type.value} | {self.owner_name}"
        )


class TwoWheeler(Vehicle):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        super().__init__(vehicle_number, owner_name, owner_type, VehicleType.TWO_WHEELER)

    @property
    def wheel_count(self) -> int:
        return 2

    @property
    def hourly_rate(self) -> float:
        return 10.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.TWO_WHEELER,)


class ThreeWheeler(Vehicle):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        super().__init__(vehicle_number, owner_name, owner_type, VehicleType.THREE_WHEELER)

    @property
    def wheel_count(self) -> int:
        return 3

    @property
    def hourly_rate(self) -> float:
        return 20.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.THREE_WHEELER,)


class Car(Vehicle):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        super().__init__(vehicle_number, owner_name, owner_type, VehicleType.CAR)

    @property
    def wheel_count(self) -> int:
        return 4

    @property
    def hourly_rate(self) -> float:
        return 30.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.COMPACT,)


class SUV(Vehicle):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        super().__init__(vehicle_number, owner_name, owner_type, VehicleType.SUV)

    @property
    def wheel_count(self) -> int:
        return 4

    @property
    def hourly_rate(self) -> float:
        return 40.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.LARGE,)


class Van(Vehicle):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        super().__init__(vehicle_number, owner_name, owner_type, VehicleType.VAN)

    @property
    def wheel_count(self) -> int:
        return 4

    @property
    def hourly_rate(self) -> float:
        return 45.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.LARGE,)


class Bus(Vehicle):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        super().__init__(vehicle_number, owner_name, owner_type, VehicleType.BUS)

    @property
    def wheel_count(self) -> int:
        return 6

    @property
    def hourly_rate(self) -> float:
        return 60.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.HEAVY,)


class ElectricTwoWheeler(TwoWheeler):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        Vehicle.__init__(
            self,
            vehicle_number,
            owner_name,
            owner_type,
            VehicleType.EV_TWO_WHEELER,
            is_electric=True,
        )

    @property
    def hourly_rate(self) -> float:
        return 15.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.EV_TWO_WHEELER,)


class ElectricCar(Car):
    def __init__(self, vehicle_number: str, owner_name: str, owner_type: OwnerType) -> None:
        Vehicle.__init__(
            self,
            vehicle_number,
            owner_name,
            owner_type,
            VehicleType.EV_CAR,
            is_electric=True,
        )

    @property
    def hourly_rate(self) -> float:
        return 45.0

    @property
    def preferred_slot_types(self) -> tuple[SlotType, ...]:
        return (SlotType.EV_CAR,)
