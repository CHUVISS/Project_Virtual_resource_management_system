from django.shortcuts import render

from models.resource import get_resources_statistics
from storage import load_allocations, load_resources, load_users


def index(request):
    resources_list = load_resources("data/resources.json")
    users_list = load_users("data/users.json")
    allocations_list = load_allocations(
        "data/allocations.json",
        resources_list,
        users_list,
    )

    active_allocations = [
        allocation for allocation in allocations_list
        if not allocation.is_cancelled
    ]
    recent_allocations = sorted(
        allocations_list,
        key=lambda allocation: allocation.allocation_date,
        reverse=True,
    )[:3]

    context = {
        "statistics": get_resources_statistics(resources_list),
        "users_count": len(users_list),
        "allocations_count": len(allocations_list),
        "active_count": len(active_allocations),
        "recent_allocations": recent_allocations,
    }

    return render(
        request,
        "homepage/index.html",
        context,
    )


def page_not_found(request, exception):
    return render(
        request,
        "homepage/page_not_found.html",
        status=404,
    )
