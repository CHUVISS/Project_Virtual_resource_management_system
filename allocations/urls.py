from django.urls import path

from . import views

urlpatterns = [
    path("", views.allocations, name="allocations"),
    path(
        "<int:allocation_id>/",
        views.allocation_detail,
        name="allocation_detail",
    ),
]
