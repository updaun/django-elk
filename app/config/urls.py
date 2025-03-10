from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

base_api = NinjaAPI()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base_api.urls),
]
