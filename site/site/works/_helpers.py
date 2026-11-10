"""Small helpers shared by several works (not a work itself)."""

from flask import request


def to_num(name):
    """Read a form field as a float, or return None if it is invalid."""
    try:
        return float(request.form.get(name, ""))
    except (ValueError, TypeError):
        return None
