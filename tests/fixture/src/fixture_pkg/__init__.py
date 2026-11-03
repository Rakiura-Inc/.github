"""A tiny package for testing the shared workflows."""

__all__ = ("__version__", "double")

__version__ = "0.0.1"


def double(value: float) -> float:
    """Return twice the value."""
    return 2 * value
