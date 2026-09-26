from datetime import date


def is_resource_available(
    allocations: list[dict], resource_id: int, allocation_date: date
) -> bool:
    """Проверить, свободен ли ресурс на указанную дату."""
    for allocation in allocations:
        if (
            allocation["resource_id"] == resource_id
            and allocation["allocation_date"] == allocation_date.isoformat()
        ):
            return False
    return True


def create_allocation(
    allocations: list[dict], resource_id: int, allocation_date: date
) -> dict:
    """Создать заявку на выделение ресурса."""
    allocation_id = max((item["id"] for item in allocations), default=0) + 1
    allocation = {
        "id": allocation_id,
        "resource_id": resource_id,
        "allocation_date": allocation_date.isoformat(),
    }
    allocations.append(allocation)
    return allocation


def cancel_allocation(allocations: list[dict], allocation_id: int) -> bool:
    """Отменить заявку по её идентификатору."""
    for index, allocation in enumerate(allocations):
        if allocation["id"] == allocation_id:
            del allocations[index]
            return True
    return False


def get_resource_status(is_available: bool) -> str:
    """Вернуть текстовый статус ресурса."""
    if is_available:
        return "Ресурс доступен для выделения"
    return "Ресурс уже занят"
