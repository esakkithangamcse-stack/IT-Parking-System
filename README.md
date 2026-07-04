# IT Park Parking System

A Python OOP project for managing parking in an IT Park for multiple vehicle categories:

- Two wheelers
- Three wheelers
- Cars
- SUVs
- Vans
- Buses
- Electric two wheelers
- Electric cars

The system supports slot allocation, ticket generation, exit processing, fee calculation, employee discounts, EV charging fees, occupancy reports, revenue reports, and a command-line menu.

## OOP Concepts Used

| Concept | Where It Is Used |
| --- | --- |
| Class and Object | Vehicle, ParkingSlot, ParkingFloor, Ticket, Payment, ParkingManager |
| Encapsulation | Vehicle fields are exposed through read-only properties |
| Inheritance | TwoWheeler, Car, Bus, ElectricCar inherit from Vehicle |
| Abstraction | Vehicle and FeeCalculator are abstract base classes |
| Polymorphism | Each vehicle class provides its own hourly rate and slot preference |
| Composition | ParkingManager contains ParkingFloor objects, which contain ParkingSlot objects |
| Enum | VehicleType, OwnerType, SlotType, PaymentMode, TicketStatus |

## Project Structure

```text
it_park_parking_system/
├── main.py
├── parking_system/
│   ├── __init__.py
│   ├── enums.py
│   ├── exceptions.py
│   ├── factory.py
│   ├── fees.py
│   ├── manager.py
│   ├── slots.py
│   ├── tickets.py
│   └── vehicles.py
└── tests/
    └── test_parking_system.py
```

## How To Run

Open a terminal in this folder and run:

```bash
python main.py
```

## How To Run Tests

```bash
python -m unittest discover -s tests
```

## Main CLI Options

```text
1. Park Vehicle
2. Exit Vehicle
3. Show Available Slots
4. Show Parked Vehicles
5. Show Reports
6. Search Vehicle
7. Show Slot Layout
0. Exit
```

## Fee Rules

| Vehicle Type | Base Rate |
| --- | ---: |
| Two Wheeler | Rs. 10/hour |
| Three Wheeler | Rs. 20/hour |
| Car | Rs. 30/hour |
| SUV | Rs. 40/hour |
| Van | Rs. 45/hour |
| Bus | Rs. 60/hour |
| EV Two Wheeler | Rs. 15/hour |
| EV Car | Rs. 45/hour |

Employee vehicles get a 50% discount, contractors get a 20% discount, VIP parking is free, and EV vehicles using charging slots pay an additional Rs. 5/hour charging fee.

## Suggested Implementation Improvements

- Add SQLite or PostgreSQL persistence.
- Add Flask or Django web UI.
- Add admin login.
- Add QR code tickets.
- Add monthly employee pass support.
- Add number plate recognition integration.
