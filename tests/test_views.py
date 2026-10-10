import os

import django
from django.test import Client
from django.test.utils import setup_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vrm.settings")
django.setup()
setup_test_environment()

client = Client()


def test_pages_open():
    for url in [
        "/",
        "/resources/",
        "/resources/?sort=ram",
        "/resources/1/",
        "/allocations/",
        "/allocations/?status=active",
        "/allocations/?status=cancelled",
        "/allocations/1/",
    ]:
        assert client.get(url).status_code == 200, url


def test_missing_objects_return_404():
    response = client.get("/resources/9999/")
    assert response.status_code == 404
    assert "Ресурс не найден" in response.content.decode()

    response = client.get("/allocations/9999/")
    assert response.status_code == 404
    assert "Заявка не найдена" in response.content.decode()


def test_templates_used():
    response = client.get("/resources/")
    names = [template.name for template in response.templates]
    assert "resources/resource_list.html" in names
    assert "base.html" in names
    assert "resources/includes/resource_card.html" in names


def test_allocation_status_filter():
    response = client.get("/allocations/?status=cancelled")
    assert all(a.is_cancelled for a in response.context["allocations"])
