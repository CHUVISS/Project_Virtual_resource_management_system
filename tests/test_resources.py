from models import Resource
from models.resource import add_resource, check_resource_capacity, find_resource


def test_resource_creation():
    resource = Resource(1, "VM-Prod-01", 4, 16, 100)
    assert resource.id == 1
    assert resource.name == "VM-Prod-01"
    assert resource.ram_gb == 16


def test_resource_is_suitable_for():
    resource = Resource(1, "VM-Prod-01", 4, 16, 100)
    assert resource.is_suitable_for(8)
    assert not resource.is_suitable_for(32)


def test_add_resource():
    resources = []
    add_resource(resources, "VM-Prod-01", 4, 16, 100)
    assert len(resources) == 1


def test_find_resource():
    resources = []
    add_resource(resources, "VM-Prod-01", 4, 16, 100)
    assert find_resource(resources, "prod")


def test_check_resource_capacity():
    resources = []
    add_resource(resources, "VM-Dev-02", 2, 8, 50)
    assert check_resource_capacity(resources, 1, 4)
