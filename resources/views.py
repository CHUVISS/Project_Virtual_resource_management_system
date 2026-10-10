from datetime import date

from django.shortcuts import render

from models.allocation import is_resource_available
from models.resource import (
    CPU_RATE,
    RAM_RATE,
    STORAGE_RATE,
    find_resource_by_id,
    sort_resources,
)
from storage import load_allocations, load_resources, load_users


def load_resources_with_allocations():
    resources_list = load_resources("data/resources.json")
    users_list = load_users("data/users.json")
    allocations_list = load_allocations(
        "data/allocations.json",
        resources_list,
        users_list,
    )
    return resources_list, allocations_list


def resources(request):
    resources_list, allocations_list = load_resources_with_allocations()
    today = date.today()

    sort = request.GET.get("sort", "")
    if sort == "ram":
        resources_list = sort_resources(resources_list)

    resource_rows = [
        {
            "resource": resource,
            "monthly_cost": resource.calculate_monthly_cost(),
            "available": is_resource_available(
                allocations_list,
                resource,
                today.isoformat(),
            ),
        }
        for resource in resources_list
    ]

    context = {
        "resource_rows": resource_rows,
        "sort": sort,
        "today": today,
    }

    return render(
        request,
        "resources/resource_list.html",
        context,
    )


def resource_detail(request, resource_id):
    resources_list, allocations_list = load_resources_with_allocations()
    resource = find_resource_by_id(resources_list, resource_id)

    context = {
        "resource": resource,
    }

    if resource is not None:
        today = date.today()
        context["today"] = today
        context["monthly_cost"] = resource.calculate_monthly_cost()
        context["cost_parts"] = [
            ("CPU", resource.cpu_cores, "ядер", CPU_RATE),
            ("RAM", resource.ram_gb, "ГБ", RAM_RATE),
            ("Хранилище", resource.storage_gb, "ГБ", STORAGE_RATE),
        ]
        context["available"] = is_resource_available(
            allocations_list,
            resource,
            today.isoformat(),
        )
        context["resource_allocations"] = [
            allocation for allocation in allocations_list
            if allocation.resource.id == resource.id
        ]

    return render(
        request,
        "resources/resource_detail.html",
        context,
        status=404 if resource is None else 200,
    )
