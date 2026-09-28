from models import Resource, User
from models.allocation import (
    cancel_allocation,
    create_allocation,
    get_resource_status,
    is_resource_available,
)
from models.resource import (
    add_resource,
    check_resource_capacity,
    find_resource,
    find_resource_by_id,
    get_resources_statistics,
)
from models.user import add_user, find_user_by_id
from storage import (
    load_allocations,
    load_resources,
    load_users,
    save_allocations,
    save_resources,
    save_users,
)
from utils import input_date, input_int

RESOURCES_FILE = "data/resources.json"
USERS_FILE = "data/users.json"
ALLOCATIONS_FILE = "data/allocations.json"

MENU = """=== Система управления виртуальными ресурсами ===
1. Показать ресурсы
2. Найти ресурс по названию
3. Проверить вместимость по RAM
4. Показать пользователей
5. Добавить пользователя
6. Проверить доступность ресурса на дату
7. Выделить ресурс (создать заявку)
8. Отменить заявку
9. Показать заявки
10. Показать статистику
0. Выход"""


def show_resources(resources: list[Resource]) -> None:
    """Вывести список ресурсов."""
    if not resources:
        print("Список ресурсов пуст")
        return
    for resource in resources:
        print(f"{resource.id}. {resource}")


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Список пользователей пуст")
        return
    for user in users:
        print(f"{user.id}. {user}")


def show_allocations(allocations: list) -> None:
    """Вывести список заявок на выделение ресурсов."""
    if not allocations:
        print("Список заявок пуст")
        return
    for allocation in allocations:
        print(allocation)


def show_statistics(resources: list[Resource]) -> None:
    """Вывести статистику по ресурсам."""
    stats = get_resources_statistics(resources)
    print(f"Ресурсов: {stats['count']}")
    print(f"Средний объём RAM: {stats['avg_ram']:.1f} ГБ")
    print(f"Суммарная стоимость аренды: {stats['total_monthly_cost']} руб./мес.")


def create_new_allocation(
    allocations: list, resources: list[Resource], users: list[User]
) -> None:
    """Пользовательский сценарий создания заявки на выделение ресурса."""
    resource_id = input_int("Идентификатор ресурса: ")
    resource = find_resource_by_id(resources, resource_id)
    if resource is None:
        print("Ресурс не найден")
        return
    user_id = input_int("Идентификатор пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден")
        return
    allocation_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    allocation = create_allocation(
        allocations, resource, allocation_date.isoformat(), user
    )
    if allocation is None:
        print("Ресурс уже занят на эту дату")
    else:
        print(f"Заявка создана: {allocation}")


def main() -> None:
    """Точка запуска приложения: цикл меню."""
    resources = load_resources(RESOURCES_FILE)
    users = load_users(USERS_FILE)
    allocations = load_allocations(ALLOCATIONS_FILE, resources, users)

    if not resources:
        add_resource(resources, "VM-Prod-01", 4, 16, 100)
        add_resource(resources, "VM-Dev-02", 2, 8, 50)
    if not users:
        add_user(users, "Иван Петров", "ivan@example.com")

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_resources(resources)
        elif choice == "2":
            query = input("Название ресурса: ")
            show_resources(find_resource(resources, query))
        elif choice == "3":
            resource_id = input_int("Идентификатор ресурса: ")
            min_ram = input_int("Минимальный объём RAM (ГБ): ")
            if check_resource_capacity(resources, resource_id, min_ram):
                print("Ресурсу достаточно RAM")
            else:
                print("Ресурсу не хватает RAM")
        elif choice == "4":
            show_users(users)
        elif choice == "5":
            name = input("Имя пользователя: ")
            email = input("Email: ")
            add_user(users, name, email)
            print("Пользователь добавлен")
        elif choice == "6":
            resource_id = input_int("Идентификатор ресурса: ")
            resource = find_resource_by_id(resources, resource_id)
            if resource is None:
                print("Ресурс не найден")
                continue
            allocation_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            available = is_resource_available(
                allocations, resource, allocation_date.isoformat()
            )
            print(get_resource_status(available))
        elif choice == "7":
            create_new_allocation(allocations, resources, users)
        elif choice == "8":
            allocation_id = input_int("Идентификатор заявки: ")
            if cancel_allocation(allocations, allocation_id):
                print("Заявка отменена")
            else:
                print("Заявка не найдена")
        elif choice == "9":
            show_allocations(allocations)
        elif choice == "10":
            show_statistics(resources)
        elif choice == "0":
            save_resources(RESOURCES_FILE, resources)
            save_users(USERS_FILE, users)
            save_allocations(ALLOCATIONS_FILE, allocations)
            print("Данные сохранены. Завершение работы.")
            break
        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
