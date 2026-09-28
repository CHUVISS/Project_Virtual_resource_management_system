from .resource import Resource
from .user import User


class Allocation:
    """Заявка на выделение виртуального ресурса пользователю."""

    def __init__(
        self,
        allocation_id: int,
        resource: Resource,
        allocation_date: str,
        user: User,
    ) -> None:
        self.id = allocation_id
        self.resource = resource
        self.allocation_date = allocation_date
        self.user = user
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить заявку."""
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"{self.id}. {self.resource.name} — {self.user.name}, "
            f"{self.allocation_date} ({status})"
        )


def is_resource_available(
    allocations: list[Allocation], resource: Resource, allocation_date: str
) -> bool:
    """Проверить, свободен ли ресурс на указанную дату."""
    for allocation in allocations:
        if (
            allocation.resource.id == resource.id
            and allocation.allocation_date == allocation_date
            and not allocation.is_cancelled
        ):
            return False
    return True


def create_allocation(
    allocations: list[Allocation],
    resource: Resource,
    allocation_date: str,
    user: User,
) -> Allocation | None:
    """Создать заявку, если ресурс свободен на указанную дату."""
    if not is_resource_available(allocations, resource, allocation_date):
        return None
    allocation_id = max((a.id for a in allocations), default=0) + 1
    allocation = Allocation(allocation_id, resource, allocation_date, user)
    allocations.append(allocation)
    return allocation


def cancel_allocation(allocations: list[Allocation], allocation_id: int) -> bool:
    """Найти заявку по идентификатору и отменить её."""
    for allocation in allocations:
        if allocation.id == allocation_id:
            allocation.cancel()
            return True
    return False


def get_resource_status(is_available: bool) -> str:
    """Вернуть текстовый статус ресурса."""
    if is_available:
        return "Ресурс доступен для выделения"
    return "Ресурс уже занят"
