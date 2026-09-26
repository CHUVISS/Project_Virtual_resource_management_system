from resources import add_resource, check_resource_capacity, find_resource


def test_add_resource():
    resources = {}
    add_resource(resources, "VM-Prod-01", 4, 16, 100)
    assert len(resources) == 1


def test_find_resource():
    resources = {}
    add_resource(resources, "VM-Prod-01", 4, 16, 100)
    assert find_resource(resources, "prod")


def test_check_resource_capacity():
    resources = {}
    add_resource(resources, "VM-Dev-02", 2, 8, 50)
    assert check_resource_capacity(resources, 1, 4)
