"""Command-line interface for the IT Park Parking System."""

from __future__ import annotations

from datetime import datetime

from parking_system.enums import OwnerType, PaymentMode, VehicleType
from parking_system.exceptions import ParkingSystemError
from parking_system.factory import create_default_it_park_manager, create_vehicle


def main() -> None:
    manager = create_default_it_park_manager()
    print(f"\nWelcome to {manager.name}")
    print(manager.address)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            park_vehicle_flow(manager)
        elif choice == "2":
            exit_vehicle_flow(manager)
        elif choice == "3":
            print_availability(manager)
        elif choice == "4":
            print_active_vehicles(manager)
        elif choice == "5":
            print_reports(manager)
        elif choice == "6":
            search_vehicle_flow(manager)
        elif choice == "7":
            print_slot_layout(manager)
        elif choice == "0":
            print("Thank you for using the IT Park Parking System.")
            break
        else:
            print("Invalid option. Please try again.")


def print_menu() -> None:
    print("\nMenu")
    print("1. Park Vehicle")
    print("2. Exit Vehicle")
    print("3. Show Available Slots")
    print("4. Show Parked Vehicles")
    print("5. Show Reports")
    print("6. Search Vehicle")
    print("7. Show Slot Layout")
    print("0. Exit")


def park_vehicle_flow(manager) -> None:
    try:
        vehicle_type = choose_enum("Vehicle Type", VehicleType)
        owner_type = choose_enum("Owner Type", OwnerType)
        vehicle_number = input("Vehicle number: ").strip()
        owner_name = input("Owner name: ").strip()

        vehicle = create_vehicle(vehicle_type, vehicle_number, owner_name, owner_type)
        ticket = manager.park_vehicle(vehicle)

        print("\nTicket Created")
        print(f"Ticket ID     : {ticket.ticket_id}")
        print(f"Vehicle       : {ticket.vehicle.to_summary()}")
        print(f"Slot          : {ticket.slot.slot_id}")
        print(f"Floor         : {ticket.slot.floor_number}")
        print(f"Entry Time    : {ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    except (ValueError, ParkingSystemError) as error:
        print(f"Unable to park vehicle: {error}")


def exit_vehicle_flow(manager) -> None:
    try:
        ticket_id = input("Ticket ID: ").strip()
        payment_mode = choose_enum("Payment Mode", PaymentMode)
        ticket, payment = manager.exit_vehicle(ticket_id, payment_mode=payment_mode)

        print("\nReceipt")
        print(f"Ticket ID     : {ticket.ticket_id}")
        print(f"Vehicle       : {ticket.vehicle.vehicle_number}")
        print(f"Slot Released : {ticket.slot.slot_id}")
        print(f"Entry Time    : {ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Exit Time     : {ticket.exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Amount Paid   : Rs. {payment.amount:.2f}")
        print(f"Payment Mode  : {payment.mode.value}")
        print(f"Payment ID    : {payment.payment_id}")
    except (ValueError, ParkingSystemError) as error:
        print(f"Unable to exit vehicle: {error}")


def print_availability(manager) -> None:
    print("\nAvailable Slots")
    for slot_type, count in manager.show_availability().items():
        print(f"{slot_type}: {count}")


def print_active_vehicles(manager) -> None:
    print("\nCurrently Parked Vehicles")
    summaries = manager.active_vehicle_summaries()
    if not summaries:
        print("No vehicles are currently parked.")
        return
    for summary in summaries:
        print(summary)


def print_reports(manager) -> None:
    occupancy = manager.occupancy_report()
    revenue = manager.revenue_report()

    print("\nOccupancy Report")
    print(f"Total Slots       : {occupancy['total_slots']}")
    print(f"Occupied Slots    : {occupancy['occupied_slots']}")
    print(f"Available Slots   : {occupancy['available_slots']}")
    print(f"Occupancy Percent : {occupancy['occupancy_percent']}%")

    print("\nRevenue Report")
    print(f"Closed Tickets       : {revenue['closed_tickets']}")
    print(f"Successful Payments  : {revenue['successful_payments']}")
    print(f"Total Revenue        : Rs. {revenue['total_revenue']:.2f}")


def search_vehicle_flow(manager) -> None:
    vehicle_number = input("Vehicle number: ").strip()
    ticket = manager.search_active_ticket_by_vehicle(vehicle_number)
    if ticket is None:
        print("Vehicle is not currently parked.")
        return
    print("\nVehicle Found")
    print(ticket.to_summary())
    print(f"Entry Time: {ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")


def print_slot_layout(manager) -> None:
    print("\nSlot Layout")
    for row in manager.slot_layout():
        print(row)


def choose_enum(label: str, enum_class):
    print(f"\n{label}")
    values = list(enum_class)
    for index, item in enumerate(values, start=1):
        print(f"{index}. {item.value}")

    selected = input(f"Choose {label.lower()}: ").strip()
    if not selected.isdigit():
        raise ValueError(f"{label} must be selected using a number.")

    index = int(selected)
    if index < 1 or index > len(values):
        raise ValueError(f"Invalid {label.lower()} selected.")
    return values[index - 1]


if __name__ == "__main__":
    main()
