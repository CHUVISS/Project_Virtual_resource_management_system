from allocations import (
    cancel_allocation,
    create_allocation,
    get_resource_status,
    is_resource_available,
)
from resources import (
    add_resource,
    calculate_monthly_cost,
    check_resource_capacity,
    find_resource,
    get_resources_statistics,
)
from storage import load_allocations, load_resources, save_allocations, save_resources
from utils import input_date, input_int

RESOURCES_FILE = "data/resources.json"
ALLOCATIONS_FILE = "data/allocations.json"

MENU = """=== Система управления виртуальными ресурсами ===
1. Показать ресурсы
2. Найти ресурс по названию
3. Проверить вместимость по RAM
4. Проверить доступность ресурса на дату
5. Выделить ресурс (создать заявку)
6. Отменить заявку
7. Показать заявки
8. Показать статистику
0. Выход"""


def show_resources(resources: dict[int, dict]) -> None:
    """Вывести список ресурсов в виде таблицы."""
    if not resources:
        print("Список ресурсов пуст")
        return
    for resource_id, data in sorted(resources.items()):
        cost = calculate_monthly_cost(
            data["cpu_cores"], data["ram_gb"], data["storage_gb"]
        )
        print(
            f"{resource_id}. {data['name']} — "
            f"{data['cpu_cores']} CPU, {data['ram_gb']} ГБ RAM, "
            f"{data['storage_gb']} ГБ, {cost} руб./мес."
        )


def show_allocations(allocations: list[dict]) -> None:
    """Вывести список заявок на выделение ресурсов."""
    if not allocations:
        print("Список заявок пуст")
        return
    for allocation in allocations:
        print(
            f"{allocation['id']}. Ресурс {allocation['resource_id']} — "
            f"{allocation['allocation_date']}"
        )


def show_statistics(resources: dict[int, dict]) -> None:
    """Вывести статистику по ресурсам."""
    stats = get_resources_statistics(resources)
    print(f"Ресурсов: {stats['count']}")
    print(f"Средний объём RAM: {stats['avg_ram']:.1f} ГБ")
    print(f"Суммарная стоимость аренды: {stats['total_monthly_cost']} руб./мес.")


def main() -> None:
    """Точка запуска приложения: цикл меню."""
    resources = load_resources(RESOURCES_FILE)
    allocations = load_allocations(ALLOCATIONS_FILE)

    if not resources:
        add_resource(resources, "VM-Prod-01", 4, 16, 100)
        add_resource(resources, "VM-Dev-02", 2, 8, 50)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_resources(resources)
        elif choice == "2":
            query = input("Название ресурса: ")
            found = find_resource(resources, query)
            show_resources({item["id"]: item for item in found})
        elif choice == "3":
            resource_id = input_int("Идентификатор ресурса: ")
            min_ram = input_int("Минимальный объём RAM (ГБ): ")
            if check_resource_capacity(resources, resource_id, min_ram):
                print("Ресурсу достаточно RAM")
            else:
                print("Ресурсу не хватает RAM")
        elif choice == "4":
            resource_id = input_int("Идентификатор ресурса: ")
            allocation_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            available = is_resource_available(
                allocations, resource_id, allocation_date
            )
            print(get_resource_status(available))
        elif choice == "5":
            resource_id = input_int("Идентификатор ресурса: ")
            allocation_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            if is_resource_available(allocations, resource_id, allocation_date):
                create_allocation(allocations, resource_id, allocation_date)
                print("Заявка создана")
            else:
                print("Ресурс уже занят на эту дату")
        elif choice == "6":
            allocation_id = input_int("Идентификатор заявки: ")
            if cancel_allocation(allocations, allocation_id):
                print("Заявка отменена")
            else:
                print("Заявка не найдена")
        elif choice == "7":
            show_allocations(allocations)
        elif choice == "8":
            show_statistics(resources)
        elif choice == "0":
            save_resources(RESOURCES_FILE, resources)
            save_allocations(ALLOCATIONS_FILE, allocations)
            print("Данные сохранены. Завершение работы.")
            break
        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
