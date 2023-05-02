from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("goods.urls")),
    path("auth/", include("users.urls")),
]
