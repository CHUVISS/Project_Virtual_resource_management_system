CPU_RATE = 500
RAM_RATE = 150
STORAGE_RATE = 10


class Resource:
    """Виртуальный ресурс (виртуальная машина)."""

    def __init__(
        self,
        resource_id: int,
        name: str,
        cpu_cores: int,
        ram_gb: int,
        storage_gb: int,
    ) -> None:
        self.id = resource_id
        self.name = name
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb
        self.storage_gb = storage_gb

    def is_suitable_for(self, min_ram: int) -> bool:
        """Проверить, хватает ли ресурсу оперативной памяти min_ram."""
        return self.ram_gb >= min_ram

    def calculate_monthly_cost(self) -> int:
        """Рассчитать ежемесячную стоимость аренды ресурса."""
        return (
            self.cpu_cores * CPU_RATE
            + self.ram_gb * RAM_RATE
            + self.storage_gb * STORAGE_RATE
        )

    @staticmethod
    def validate_ram(ram_gb: int) -> bool:
        """Проверить корректность значения объёма RAM."""
        return ram_gb > 0

    def __str__(self) -> str:
        return (
            f"{self.name} — {self.cpu_cores} CPU, {self.ram_gb} ГБ RAM, "
            f"{self.storage_gb} ГБ, {self.calculate_monthly_cost()} руб./мес."
        )


def add_resource(
    resources: list[Resource],
    name: str,
    cpu_cores: int,
    ram_gb: int,
    storage_gb: int,
) -> Resource:
    """Создать объект Resource и добавить его в коллекцию."""
    resource_id = max((r.id for r in resources), default=0) + 1
    resource = Resource(resource_id, name, cpu_cores, ram_gb, storage_gb)
    resources.append(resource)
    return resource


def find_resource(resources: list[Resource], query: str) -> list[Resource]:
    """Найти ресурсы, в названии которых встречается подстрока query."""
    query = query.lower()
    return [r for r in resources if query in r.name.lower()]


def find_resource_by_id(
    resources: list[Resource], resource_id: int
) -> Resource | None:
    """Найти ресурс по идентификатору."""
    for resource in resources:
        if resource.id == resource_id:
            return resource
    return None


def check_resource_capacity(
    resources: list[Resource], resource_id: int, min_ram: int
) -> bool:
    """Найти ресурс и проверить его вместимость по RAM."""
    resource = find_resource_by_id(resources, resource_id)
    if resource is None:
        return False
    return resource.is_suitable_for(min_ram)


def filter_resources_by_ram(
    resources: list[Resource], min_ram: int
) -> list[Resource]:
    """Отобрать ресурсы, у которых объём RAM не меньше min_ram."""
    return [r for r in resources if r.is_suitable_for(min_ram)]


def sort_resources(resources: list[Resource]) -> list[Resource]:
    """Отсортировать ресурсы по объёму RAM по убыванию."""
    return sorted(resources, key=lambda r: r.ram_gb, reverse=True)


def get_resources_statistics(resources: list[Resource]) -> dict:
    """Собрать статистику по имеющимся ресурсам."""
    if not resources:
        return {"count": 0, "avg_ram": 0, "total_monthly_cost": 0}
    ram_values = [r.ram_gb for r in resources]
    total_cost = sum(r.calculate_monthly_cost() for r in resources)
    return {
        "count": len(resources),
        "avg_ram": sum(ram_values) / len(ram_values),
        "total_monthly_cost": total_cost,
    }
