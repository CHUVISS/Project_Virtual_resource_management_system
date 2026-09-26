CPU_RATE = 500
RAM_RATE = 150
STORAGE_RATE = 10


def add_resource(
    resources: dict[int, dict],
    name: str,
    cpu_cores: int,
    ram_gb: int,
    storage_gb: int,
) -> int:
    """Добавить виртуальный ресурс и вернуть его идентификатор."""
    resource_id = max(resources.keys(), default=0) + 1
    resources[resource_id] = {
        "name": name,
        "cpu_cores": cpu_cores,
        "ram_gb": ram_gb,
        "storage_gb": storage_gb,
        "is_available": True,
    }
    return resource_id


def find_resource(resources: dict[int, dict], query: str) -> list[dict]:
    """Найти ресурсы, в названии которых встречается подстрока query."""
    query = query.lower()
    return [
        {"id": resource_id, **data}
        for resource_id, data in resources.items()
        if query in data["name"].lower()
    ]


def check_resource_capacity(
    resources: dict[int, dict], resource_id: int, min_ram: int
) -> bool:
    """Проверить, хватает ли ресурсу оперативной памяти min_ram."""
    resource = resources.get(resource_id)
    if resource is None:
        return False
    return resource["ram_gb"] >= min_ram


def filter_resources_by_ram(
    resources: dict[int, dict], min_ram: int
) -> list[dict]:
    """Отобрать ресурсы, у которых объём RAM не меньше min_ram."""
    return [
        {"id": resource_id, **data}
        for resource_id, data in resources.items()
        if data["ram_gb"] >= min_ram
    ]


def sort_resources(resources: dict[int, dict]) -> list[dict]:
    """Отсортировать ресурсы по объёму RAM по убыванию."""
    items = [{"id": resource_id, **data} for resource_id, data in resources.items()]
    return sorted(items, key=lambda item: item["ram_gb"], reverse=True)


def calculate_monthly_cost(cpu_cores: int, ram_gb: int, storage_gb: int) -> int:
    """Рассчитать ежемесячную стоимость аренды ресурса."""
    return cpu_cores * CPU_RATE + ram_gb * RAM_RATE + storage_gb * STORAGE_RATE


def get_resources_statistics(resources: dict[int, dict]) -> dict:
    """Собрать статистику по имеющимся ресурсам."""
    if not resources:
        return {"count": 0, "avg_ram": 0, "total_monthly_cost": 0}
    ram_values = [data["ram_gb"] for data in resources.values()]
    total_cost = sum(
        calculate_monthly_cost(data["cpu_cores"], data["ram_gb"], data["storage_gb"])
        for data in resources.values()
    )
    return {
        "count": len(resources),
        "avg_ram": sum(ram_values) / len(ram_values),
        "total_monthly_cost": total_cost,
    }
