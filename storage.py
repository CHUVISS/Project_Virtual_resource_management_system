import json

from models import Allocation, Resource, User
from models.resource import find_resource_by_id
from models.user import find_user_by_id


def load_resources(filename: str) -> list[Resource]:
    """Загрузить ресурсы из JSON-файла и создать объекты Resource."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_resources = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return [
        Resource(
            item["id"],
            item["name"],
            item["cpu_cores"],
            item["ram_gb"],
            item["storage_gb"],
        )
        for item in raw_resources
    ]


def save_resources(filename: str, resources: list[Resource]) -> None:
    """Сохранить объекты Resource в JSON-файл."""
    raw_resources = [
        {
            "id": r.id,
            "name": r.name,
            "cpu_cores": r.cpu_cores,
            "ram_gb": r.ram_gb,
            "storage_gb": r.storage_gb,
        }
        for r in resources
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_resources, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON-файла и создать объекты User."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return [User.from_data(item) for item in raw_users]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить объекты User в JSON-файл."""
    raw_users = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_users, file, ensure_ascii=False, indent=2)


def load_allocations(
    filename: str, resources: list[Resource], users: list[User]
) -> list[Allocation]:
    """Загрузить заявки из JSON, связав их с объектами Resource и User."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_allocations = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    allocations = []
    for item in raw_allocations:
        resource = find_resource_by_id(resources, item["resource_id"])
        user = find_user_by_id(users, item["user_id"])
        if resource is None or user is None:
            continue
        allocation = Allocation(
            item["id"], resource, item["allocation_date"], user
        )
        allocation.is_cancelled = item["is_cancelled"]
        allocations.append(allocation)
    return allocations


def save_allocations(filename: str, allocations: list[Allocation]) -> None:
    """Сохранить заявки в JSON, заменив объекты их идентификаторами."""
    raw_allocations = [
        {
            "id": a.id,
            "resource_id": a.resource.id,
            "allocation_date": a.allocation_date,
            "user_id": a.user.id,
            "is_cancelled": a.is_cancelled,
        }
        for a in allocations
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_allocations, file, ensure_ascii=False, indent=2)
