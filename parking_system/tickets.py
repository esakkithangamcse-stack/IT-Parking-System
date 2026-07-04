"""Ticket and payment models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from parking_system.enums import PaymentMode, PaymentStatus, TicketStatus
from parking_system.slots import ParkingSlot
from parking_system.vehicles import Vehicle


@dataclass
class Ticket:
    ticket_id: str
    vehicle: Vehicle
    slot: ParkingSlot
    entry_time: datetime = field(default_factory=datetime.now)
    exit_time: datetime | None = None
    status: TicketStatus = TicketStatus.ACTIVE
    amount: float = 0.0

    def close(self, exit_time: datetime, amount: float) -> None:
        self.exit_time = exit_time
        self.amount = amount
        self.status = TicketStatus.CLOSED

    def to_summary(self) -> str:
        return (
            f"{self.ticket_id} | {self.vehicle.vehicle_number} | "
            f"{self.vehicle.vehicle_type.value} | Slot {self.slot.slot_id} | "
            f"{self.status.value}"
        )


@dataclass
class Payment:
    payment_id: str
    ticket_id: str
    amount: float
    mode: PaymentMode
    status: PaymentStatus = PaymentStatus.SUCCESS
    paid_at: datetime = field(default_factory=datetime.now)
