"""Fee calculation using abstraction and polymorphic vehicle rates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from math import ceil

from parking_system.enums import OwnerType
from parking_system.tickets import Ticket


class FeeCalculator(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket, exit_time: datetime | None = None) -> float:
        """Calculate final payable fee for a ticket."""


class ITParkFeeCalculator(FeeCalculator):
    """Default IT park hourly fee calculator."""

    OWNER_DISCOUNTS = {
        OwnerType.EMPLOYEE: 0.50,
        OwnerType.CONTRACTOR: 0.20,
        OwnerType.VIP: 1.00,
        OwnerType.VISITOR: 0.00,
    }

    EV_CHARGING_RATE_PER_HOUR = 5.0

    def calculate_fee(self, ticket: Ticket, exit_time: datetime | None = None) -> float:
        final_exit_time = exit_time or datetime.now()
        duration_seconds = (final_exit_time - ticket.entry_time).total_seconds()
        chargeable_hours = max(1, ceil(duration_seconds / 3600))

        base_fee = ticket.vehicle.calculate_base_fee(chargeable_hours)
        discount_rate = self.OWNER_DISCOUNTS.get(ticket.vehicle.owner_type, 0.0)
        discounted_fee = base_fee * (1 - discount_rate)

        charging_fee = 0.0
        if ticket.vehicle.is_electric and ticket.slot.has_charger:
            charging_fee = self.EV_CHARGING_RATE_PER_HOUR * chargeable_hours

        return round(discounted_fee + charging_fee, 2)

    def chargeable_hours(self, ticket: Ticket, exit_time: datetime | None = None) -> int:
        final_exit_time = exit_time or datetime.now()
        duration_seconds = (final_exit_time - ticket.entry_time).total_seconds()
        return max(1, ceil(duration_seconds / 3600))
