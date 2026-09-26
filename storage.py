import json


def load_resources(filename: str) -> dict[int, dict]:
    """Загрузить ресурсы из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_resources = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {
        item["id"]: {key: value for key, value in item.items() if key != "id"}
        for item in raw_resources
    }


def save_resources(filename: str, resources: dict[int, dict]) -> None:
    """Сохранить ресурсы в JSON-файл."""
    raw_resources = [
        {"id": resource_id, **data} for resource_id, data in resources.items()
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_resources, file, ensure_ascii=False, indent=2)


def load_allocations(filename: str) -> list[dict]:
    """Загрузить заявки на выделение ресурсов из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_allocations(filename: str, allocations: list[dict]) -> None:
    """Сохранить заявки на выделение ресурсов в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(allocations, file, ensure_ascii=False, indent=2)
