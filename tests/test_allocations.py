from datetime import date

from allocations import create_allocation, is_resource_available


def test_is_resource_available():
    allocations = []
    assert is_resource_available(allocations, 1, date(2026, 9, 15))


def test_duplicate_allocation_forbidden():
    allocations = []
    create_allocation(allocations, 1, date(2026, 9, 15))
    assert not is_resource_available(allocations, 1, date(2026, 9, 15))
