from django.urls import path

from . import views

app_name = "allocations"

urlpatterns = [
    path("", views.allocations, name="list"),
    path(
        "<int:allocation_id>/",
        views.allocation_detail,
        name="detail",
    ),
]
