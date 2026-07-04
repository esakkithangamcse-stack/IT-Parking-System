"""Factory helpers for creating vehicles and a sample IT park layout."""

from __future__ import annotations

from parking_system.enums import OwnerType, SlotType, VehicleType
from parking_system.manager import ParkingManager
from parking_system.slots import ParkingFloor, ParkingSlot
from parking_system.vehicles import (
    Bus,
    Car,
    ElectricCar,
    ElectricTwoWheeler,
    SUV,
    ThreeWheeler,
    TwoWheeler,
    Van,
    Vehicle,
)


def create_vehicle(
    vehicle_type: VehicleType,
    vehicle_number: str,
    owner_name: str,
    owner_type: OwnerType,
) -> Vehicle:
    vehicle_map = {
        VehicleType.TWO_WHEELER: TwoWheeler,
        VehicleType.THREE_WHEELER: ThreeWheeler,
        VehicleType.CAR: Car,
        VehicleType.SUV: SUV,
        VehicleType.VAN: Van,
        VehicleType.BUS: Bus,
        VehicleType.EV_TWO_WHEELER: ElectricTwoWheeler,
        VehicleType.EV_CAR: ElectricCar,
    }
    return vehicle_map[vehicle_type](vehicle_number, owner_name, owner_type)


def create_default_it_park_manager() -> ParkingManager:
    floors = [
        ParkingFloor(
            floor_number=1,
            slots=[
                *_build_slots(1, SlotType.TWO_WHEELER, 8),
                *_build_slots(1, SlotType.THREE_WHEELER, 3),
                *_build_slots(1, SlotType.COMPACT, 8),
                *_build_slots(1, SlotType.EV_TWO_WHEELER, 4),
                *_build_slots(1, SlotType.EV_CAR, 3),
            ],
        ),
        ParkingFloor(
            floor_number=2,
            slots=[
                *_build_slots(2, SlotType.COMPACT, 10),
                *_build_slots(2, SlotType.LARGE, 6),
                *_build_slots(2, SlotType.HEAVY, 2),
            ],
        ),
        ParkingFloor(
            floor_number=3,
            slots=[
                *_build_slots(3, SlotType.TWO_WHEELER, 8),
                *_build_slots(3, SlotType.COMPACT, 8),
                *_build_slots(3, SlotType.LARGE, 4),
                *_build_slots(3, SlotType.EV_CAR, 3),
            ],
        ),
    ]

    return ParkingManager(
        name="IT Park Multi Wheeler Parking",
        address="Main Gate, IT Park Campus",
        floors=floors,
    )


def _build_slots(floor_number: int, slot_type: SlotType, count: int) -> list[ParkingSlot]:
    prefix = {
        SlotType.TWO_WHEELER: "TW",
        SlotType.THREE_WHEELER: "TH",
        SlotType.COMPACT: "CP",
        SlotType.LARGE: "LG",
        SlotType.HEAVY: "HV",
        SlotType.EV_TWO_WHEELER: "ET",
        SlotType.EV_CAR: "EC",
    }[slot_type]
    return [
        ParkingSlot(
            slot_id=f"F{floor_number}-{prefix}-{index:03d}",
            floor_number=floor_number,
            slot_type=slot_type,
        )
        for index in range(1, count + 1)
    ]
