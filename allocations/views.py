from django.http import HttpResponse

from homepage.views import page
from models.allocation import find_allocation_by_id
from storage import load_allocations, load_resources, load_users


def allocations(request):
    resources_list = load_resources("data/resources.json")
    users_list = load_users("data/users.json")
    allocations_list = load_allocations(
        "data/allocations.json",
        resources_list,
        users_list,
    )

    items = ""
    for allocation in allocations_list:
        status = "отменена" if allocation.is_cancelled else "активна"
        badge = "bg-secondary" if allocation.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/allocations/{allocation.id}/">
                {allocation.resource.name} – {allocation.allocation_date}
            </a>
            <span class="badge {badge}">
                {status}
            </span>
        </li>
        """
    content = f"""
    <h1>Заявки</h1>
    <ul class="list-group">
        {items}
    </ul>
    """
    return HttpResponse(
        page("Заявки", content)
    )


def allocation_detail(request, allocation_id):
    resources_list = load_resources("data/resources.json")

    users_list = load_users("data/users.json")
    allocations_list = load_allocations(
        "data/allocations.json",
        resources_list,
        users_list,
    )
    allocation = find_allocation_by_id(
        allocations_list,
        allocation_id,
    )
    if allocation is None:
        content = """
        <h1 class="text-danger">
            Заявка не найдена
        </h1>
        <a href="/allocations/"
           class="btn btn-outline-secondary">
            ← к списку заявок
        </a>
        """
        return HttpResponse(
            page("Заявка не найдена", content),
            status=404,
        )

    status = "отменена" if allocation.is_cancelled else "активна"
    badge = "bg-secondary" if allocation.is_cancelled else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Заявка №{allocation.id}
            </h5>
            <p class="card-text">
                Ресурс: {allocation.resource.name}
            </p>
            <p class="card-text">
                Дата: {allocation.allocation_date}
            </p>
            <p class="card-text">
                Пользователь: {allocation.user.name}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">
                    {status}
                </span>
            </p>
            <a href="/allocations/"
               class="btn btn-outline-secondary">
                ← к списку заявок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(
            f"Заявка №{allocation.id}",
            content,
        ),
        status=200,
    )
