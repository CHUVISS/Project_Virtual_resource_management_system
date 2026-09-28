from models import Resource, User
from models.allocation import create_allocation, is_resource_available


def test_allocation_creation():
    resource = Resource(1, "VM-Prod-01", 4, 16, 100)
    user = User(1, "Иван Петров", "ivan@example.com")
    allocations = []
    allocation = create_allocation(allocations, resource, "2026-09-15", user)
    assert allocation is not None
    assert allocation.resource is resource
    assert allocation.user is user


def test_allocation_cancel():
    resource = Resource(1, "VM-Prod-01", 4, 16, 100)
    user = User(1, "Иван Петров", "ivan@example.com")
    allocations = []
    allocation = create_allocation(allocations, resource, "2026-09-15", user)
    allocation.cancel()
    assert allocation.is_cancelled


def test_cancelled_allocation_frees_resource():
    resource = Resource(1, "VM-Prod-01", 4, 16, 100)
    user = User(1, "Иван Петров", "ivan@example.com")
    allocations = []
    allocation = create_allocation(allocations, resource, "2026-09-15", user)
    allocation.cancel()
    assert is_resource_available(allocations, resource, "2026-09-15")


def test_duplicate_allocation_forbidden():
    resource = Resource(1, "VM-Prod-01", 4, 16, 100)
    user = User(1, "Иван Петров", "ivan@example.com")
    allocations = []
    create_allocation(allocations, resource, "2026-09-15", user)
    second = create_allocation(allocations, resource, "2026-09-15", user)
    assert second is None
