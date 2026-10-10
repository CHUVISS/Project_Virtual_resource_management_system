from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("resources/", include("resources.urls")),
    path("allocations/", include("allocations.urls")),
]
