from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.allocation import is_resource_available
from models.resource import find_resource_by_id
from storage import load_allocations, load_resources, load_users


def resources(request):
    items = ""
    for resource in load_resources("data/resources.json"):
        text = (
            f"{resource.name} – {resource.cpu_cores} CPU, "
            f"{resource.ram_gb} ГБ RAM, {resource.storage_gb} ГБ"
        )
        items += (
            '<li class="list-group-item">'
            f'<a href="/resources/{resource.id}/">{text}</a>'
            "</li>"
        )
    content = f"""
    <h1>Ресурсы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Ресурсы", content))


def resource_detail(request, resource_id):
    resources_list = load_resources("data/resources.json")

    resource = find_resource_by_id(resources_list, resource_id)

    if resource is None:
        content = """
        <h1 class="text-danger">Ресурс не найден</h1>
        <a href="/resources/" class="btn btn-outline-secondary">
            ← к списку ресурсов
        </a>
        """

        return HttpResponse(
            page("Ресурс не найден", content),
            status=404,
        )
    users_list = load_users("data/users.json")
    allocations_list = load_allocations(
        "data/allocations.json",
        resources_list,
        users_list,
    )
    available = is_resource_available(
        allocations_list,
        resource,
        date.today().isoformat(),
    )
    status = "доступен" if available else "занят"
    badge = "bg-success" if available else "bg-danger"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{resource.name}</h5>

            <p class="card-text">
                <strong>ID:</strong> {resource.id}
            </p>

            <p class="card-text">
                <strong>CPU:</strong> {resource.cpu_cores} ядер
            </p>

            <p class="card-text">
                <strong>RAM:</strong> {resource.ram_gb} ГБ
            </p>

            <p class="card-text">
                <strong>Хранилище:</strong> {resource.storage_gb} ГБ
            </p>

            <p class="card-text">
                <strong>Стоимость аренды:</strong>
                {resource.calculate_monthly_cost()} руб./мес.
            </p>

            <p class="card-text">
                Доступность на текущую дату:
                <span class="badge {badge}">
                    {status}
                </span>
            </p>

            <a href="/resources/"
               class="btn btn-outline-secondary">
                ← к списку ресурсов
            </a>
        </div>
    </div>
    """

    return HttpResponse(
        page(resource.name, content),
        status=200,
    )
