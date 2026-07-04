"""Unit tests for the IT Park Parking System."""

from datetime import datetime, timedelta
from unittest import TestCase, main

from parking_system.enums import OwnerType, PaymentMode, SlotType, VehicleType
from parking_system.exceptions import DuplicateVehicleError, ParkingFullError
from parking_system.factory import create_default_it_park_manager, create_vehicle
from parking_system.manager import ParkingManager
from parking_system.slots import ParkingFloor, ParkingSlot


class ParkingSystemTests(TestCase):
    def test_vehicle_can_be_parked_and_ticket_is_created(self) -> None:
        manager = create_default_it_park_manager()
        vehicle = create_vehicle(
            VehicleType.TWO_WHEELER,
            "TN01AB1234",
            "Arun",
            OwnerType.EMPLOYEE,
        )

        ticket = manager.park_vehicle(vehicle)

        self.assertTrue(ticket.ticket_id.startswith("TKT-"))
        self.assertEqual(ticket.vehicle.vehicle_number, "TN01AB1234")
        self.assertFalse(ticket.slot.is_available)

    def test_duplicate_vehicle_is_not_allowed(self) -> None:
        manager = create_default_it_park_manager()
        vehicle = create_vehicle(VehicleType.CAR, "TN09CD5678", "Meena", OwnerType.VISITOR)

        manager.park_vehicle(vehicle)

        with self.assertRaises(DuplicateVehicleError):
            manager.park_vehicle(vehicle)

    def test_parking_full_error_when_no_suitable_slot_exists(self) -> None:
        manager = ParkingManager(
            name="Small Test Lot",
            address="Test",
            floors=[
                ParkingFloor(
                    floor_number=1,
                    slots=[ParkingSlot("F1-TW-001", 1, SlotType.TWO_WHEELER)],
                )
            ],
        )
        first = create_vehicle(VehicleType.TWO_WHEELER, "TN01AA1111", "A", OwnerType.VISITOR)
        second = create_vehicle(VehicleType.TWO_WHEELER, "TN01AA2222", "B", OwnerType.VISITOR)

        manager.park_vehicle(first)

        with self.assertRaises(ParkingFullError):
            manager.park_vehicle(second)

    def test_exit_vehicle_calculates_fee_and_releases_slot(self) -> None:
        manager = create_default_it_park_manager()
        vehicle = create_vehicle(VehicleType.CAR, "TN10EF9012", "Dinesh", OwnerType.VISITOR)
        ticket = manager.park_vehicle(vehicle)
        ticket.entry_time = datetime.now() - timedelta(hours=2, minutes=10)

        closed_ticket, payment = manager.exit_vehicle(ticket.ticket_id, PaymentMode.UPI)

        self.assertEqual(closed_ticket.amount, 90.0)
        self.assertEqual(payment.amount, 90.0)
        self.assertTrue(closed_ticket.slot.is_available)
        self.assertEqual(manager.revenue_report()["total_revenue"], 90.0)

    def test_employee_discount_is_applied(self) -> None:
        manager = create_default_it_park_manager()
        vehicle = create_vehicle(VehicleType.SUV, "TN22GH3456", "Priya", OwnerType.EMPLOYEE)
        ticket = manager.park_vehicle(vehicle)
        ticket.entry_time = datetime.now() - timedelta(hours=1, minutes=5)

        closed_ticket, payment = manager.exit_vehicle(ticket.ticket_id, PaymentMode.COMPANY_ACCOUNT)

        self.assertEqual(closed_ticket.amount, 40.0)
        self.assertEqual(payment.amount, 40.0)

    def test_ev_vehicle_gets_ev_slot_and_charging_fee(self) -> None:
        manager = create_default_it_park_manager()
        vehicle = create_vehicle(VehicleType.EV_CAR, "TN44EV2026", "Kavya", OwnerType.VISITOR)
        ticket = manager.park_vehicle(vehicle)
        ticket.entry_time = datetime.now() - timedelta(minutes=30)

        closed_ticket, payment = manager.exit_vehicle(ticket.ticket_id, PaymentMode.CARD)

        self.assertEqual(ticket.slot.slot_type, SlotType.EV_CAR)
        self.assertEqual(closed_ticket.amount, 50.0)
        self.assertEqual(payment.amount, 50.0)


if __name__ == "__main__":
    main()
