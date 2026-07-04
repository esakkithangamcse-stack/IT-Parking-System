"""Parking slot and floor models."""

from __future__ import annotations

from dataclasses import dataclass, field

from parking_system.enums import SlotType
from parking_system.exceptions import SlotUnavailableError
from parking_system.vehicles import Vehicle


@dataclass
class ParkingSlot:
    slot_id: str
    floor_number: int
    slot_type: SlotType
    is_reserved: bool = False
    assigned_vehicle: Vehicle | None = field(default=None, init=False)

    @property
    def is_available(self) -> bool:
        return self.assigned_vehicle is None

    @property
    def has_charger(self) -> bool:
        return self.slot_type in {SlotType.EV_TWO_WHEELER, SlotType.EV_CAR}

    def can_fit(self, vehicle: Vehicle) -> bool:
        return self.is_available and self.slot_type in vehicle.preferred_slot_types

    def assign_vehicle(self, vehicle: Vehicle) -> None:
        if not self.can_fit(vehicle):
            raise SlotUnavailableError(
                f"Slot {self.slot_id} cannot accept {vehicle.vehicle_type.value}."
            )
        self.assigned_vehicle = vehicle

    def release_vehicle(self) -> None:
        self.assigned_vehicle = None

    def to_summary(self) -> str:
        status = "Available" if self.is_available else f"Occupied by {self.assigned_vehicle.vehicle_number}"
        reserved = "Reserved" if self.is_reserved else "General"
        return f"{self.slot_id} | Floor {self.floor_number} | {self.slot_type.value} | {reserved} | {status}"


@dataclass
class ParkingFloor:
    floor_number: int
    slots: list[ParkingSlot]

    def find_available_slot(self, vehicle: Vehicle) -> ParkingSlot | None:
        for slot in self.slots:
            if slot.can_fit(vehicle):
                return slot
        return None

    def availability_count(self) -> dict[SlotType, int]:
        counts = {slot_type: 0 for slot_type in SlotType}
        for slot in self.slots:
            if slot.is_available:
                counts[slot.slot_type] += 1
        return counts

    def occupied_slots(self) -> list[ParkingSlot]:
        return [slot for slot in self.slots if not slot.is_available]
