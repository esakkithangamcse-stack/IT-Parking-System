"""Enums used across the parking system."""

from enum import Enum


class VehicleType(Enum):
    TWO_WHEELER = "Two Wheeler"
    THREE_WHEELER = "Three Wheeler"
    CAR = "Car"
    SUV = "SUV"
    VAN = "Van"
    BUS = "Bus"
    EV_TWO_WHEELER = "EV Two Wheeler"
    EV_CAR = "EV Car"


class OwnerType(Enum):
    EMPLOYEE = "Employee"
    VISITOR = "Visitor"
    CONTRACTOR = "Contractor"
    VIP = "VIP"


class SlotType(Enum):
    TWO_WHEELER = "Two Wheeler Slot"
    THREE_WHEELER = "Three Wheeler Slot"
    COMPACT = "Compact Car Slot"
    LARGE = "Large Vehicle Slot"
    HEAVY = "Heavy Vehicle Slot"
    EV_TWO_WHEELER = "EV Two Wheeler Charging Slot"
    EV_CAR = "EV Car Charging Slot"


class TicketStatus(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"


class PaymentMode(Enum):
    CASH = "Cash"
    CARD = "Card"
    UPI = "UPI"
    COMPANY_ACCOUNT = "Company Account"


class PaymentStatus(Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
