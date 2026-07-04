"""Main parking manager service."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from parking_system.enums import PaymentMode, SlotType
from parking_system.exceptions import DuplicateVehicleError, InvalidTicketError, ParkingFullError
from parking_system.fees import FeeCalculator, ITParkFeeCalculator
from parking_system.slots import ParkingFloor, ParkingSlot
from parking_system.tickets import Payment, Ticket
from parking_system.vehicles import Vehicle


@dataclass
class ParkingManager:
    name: str
    address: str
    floors: list[ParkingFloor]
    fee_calculator: FeeCalculator = field(default_factory=ITParkFeeCalculator)
    active_tickets: dict[str, Ticket] = field(default_factory=dict)
    completed_tickets: list[Ticket] = field(default_factory=list)
    payments: list[Payment] = field(default_factory=list)

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        if self.search_active_ticket_by_vehicle(vehicle.vehicle_number):
            raise DuplicateVehicleError(f"Vehicle {vehicle.vehicle_number} is already parked.")

        slot = self._find_suitable_slot(vehicle)
        if slot is None:
            raise ParkingFullError(f"No suitable slot available for {vehicle.vehicle_type.value}.")

        slot.assign_vehicle(vehicle)
        ticket = Ticket(ticket_id=self._generate_ticket_id(), vehicle=vehicle, slot=slot)
        self.active_tickets[ticket.ticket_id] = ticket
        return ticket

    def exit_vehicle(
        self,
        ticket_id: str,
        payment_mode: PaymentMode = PaymentMode.CASH,
        exit_time: datetime | None = None,
    ) -> tuple[Ticket, Payment]:
        ticket = self.active_tickets.get(ticket_id.strip().upper())
        if ticket is None:
            raise InvalidTicketError(f"Active ticket {ticket_id} was not found.")

        final_exit_time = exit_time or datetime.now()
        fee = self.fee_calculator.calculate_fee(ticket, final_exit_time)
        payment = Payment(
            payment_id=self._generate_payment_id(),
            ticket_id=ticket.ticket_id,
            amount=fee,
            mode=payment_mode,
        )

        ticket.close(final_exit_time, fee)
        ticket.slot.release_vehicle()
        self.completed_tickets.append(ticket)
        self.payments.append(payment)
        del self.active_tickets[ticket.ticket_id]
        return ticket, payment

    def show_availability(self) -> dict[str, int]:
        total = {slot_type.value: 0 for slot_type in SlotType}
        for floor in self.floors:
            for slot_type, count in floor.availability_count().items():
                total[slot_type.value] += count
        return total

    def active_vehicle_summaries(self) -> list[str]:
        return [ticket.to_summary() for ticket in self.active_tickets.values()]

    def search_active_ticket_by_vehicle(self, vehicle_number: str) -> Ticket | None:
        normalized_number = vehicle_number.strip().upper()
        for ticket in self.active_tickets.values():
            if ticket.vehicle.vehicle_number == normalized_number:
                return ticket
        return None

    def occupancy_report(self) -> dict[str, int | float]:
        total_slots = sum(len(floor.slots) for floor in self.floors)
        occupied_slots = sum(len(floor.occupied_slots()) for floor in self.floors)
        available_slots = total_slots - occupied_slots
        occupancy_percent = round((occupied_slots / total_slots) * 100, 2) if total_slots else 0.0
        return {
            "total_slots": total_slots,
            "occupied_slots": occupied_slots,
            "available_slots": available_slots,
            "occupancy_percent": occupancy_percent,
        }

    def revenue_report(self) -> dict[str, float | int]:
        total_revenue = round(sum(payment.amount for payment in self.payments), 2)
        return {
            "closed_tickets": len(self.completed_tickets),
            "successful_payments": len(self.payments),
            "total_revenue": total_revenue,
        }

    def slot_layout(self) -> list[str]:
        rows: list[str] = []
        for floor in self.floors:
            rows.append(f"Floor {floor.floor_number}")
            rows.extend(slot.to_summary() for slot in floor.slots)
        return rows

    def _find_suitable_slot(self, vehicle: Vehicle) -> ParkingSlot | None:
        for floor in self.floors:
            slot = floor.find_available_slot(vehicle)
            if slot is not None:
                return slot
        return None

    @staticmethod
    def _generate_ticket_id() -> str:
        return f"TKT-{uuid4().hex[:8].upper()}"

    @staticmethod
    def _generate_payment_id() -> str:
        return f"PAY-{uuid4().hex[:8].upper()}"
