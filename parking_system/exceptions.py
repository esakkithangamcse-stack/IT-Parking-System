"""Custom exceptions for clear business-rule failures."""


class ParkingSystemError(Exception):
    """Base exception for the parking system."""


class ParkingFullError(ParkingSystemError):
    """Raised when no suitable parking slot is available."""


class DuplicateVehicleError(ParkingSystemError):
    """Raised when the same vehicle is already parked."""


class InvalidTicketError(ParkingSystemError):
    """Raised when a ticket is missing, closed, or invalid."""


class SlotUnavailableError(ParkingSystemError):
    """Raised when a slot cannot accept a vehicle."""
