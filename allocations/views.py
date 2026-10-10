from django.shortcuts import render

from models.allocation import find_allocation_by_id
from storage import load_allocations, load_resources, load_users

STATUS_FILTERS = [
    ("", "Все"),
    ("active", "Активные"),
    ("cancelled", "Отменённые"),
]


def load_all_allocations():
    resources_list = load_resources("data/resources.json")
    users_list = load_users("data/users.json")
    return load_allocations(
        "data/allocations.json",
        resources_list,
        users_list,
    )


def allocations(request):
    allocations_list = load_all_allocations()

    status = request.GET.get("status", "")
    if status == "active":
        shown = [a for a in allocations_list if not a.is_cancelled]
    elif status == "cancelled":
        shown = [a for a in allocations_list if a.is_cancelled]
    else:
        status = ""
        shown = allocations_list

    context = {
        "allocations": shown,
        "total_count": len(allocations_list),
        "status": status,
        "status_filters": STATUS_FILTERS,
    }

    return render(
        request,
        "allocations/allocation_list.html",
        context,
    )


def allocation_detail(request, allocation_id):
    allocations_list = load_all_allocations()

    allocation = find_allocation_by_id(
        allocations_list,
        allocation_id,
    )

    context = {
        "allocation": allocation,
    }

    return render(
        request,
        "allocations/allocation_detail.html",
        context,
        status=404 if allocation is None else 200,
    )
