from datetime import date

CPU_RATE = 500
RAM_RATE = 150
STORAGE_RATE = 10

resource_name = "VM-Prod-01"
cpu_cores = 4
ram_gb = 16
storage_gb = 100
allocation_date = date(2026, 9, 15)
is_available = True


def get_resource_status(is_available):
    if is_available:
        return "Ресурс доступен для выделения"
    return "Ресурс уже занят"


def calculate_monthly_cost(cpu_cores, ram_gb, storage_gb):
    cost = cpu_cores * CPU_RATE + ram_gb * RAM_RATE + storage_gb * STORAGE_RATE
    return cost


def check_capacity(requested_ram, available_ram):
    if requested_ram <= available_ram:
        return True
    return False


print(f"Ресурс: {resource_name}")
print(f"CPU: {cpu_cores} ядер")
print(f"RAM: {ram_gb} ГБ")
print(f"Хранилище: {storage_gb} ГБ")
print(f"Дата выделения: {allocation_date}")
print(get_resource_status(is_available))

monthly_cost = calculate_monthly_cost(cpu_cores, ram_gb, storage_gb)
print(f"Стоимость аренды в месяц: {int(monthly_cost)} руб.")

requested_ram = int("32")
capacity_ok = check_capacity(requested_ram, ram_gb)
print(f"Запрошено RAM: {requested_ram} ГБ")

if capacity_ok:
    print("Достаточно ресурсов для расширения")
else:
    print("Недостаточно ресурсов для расширения")
