from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

base_api = NinjaAPI()


@base_api.get("")
async def home(request):
    return {"hello": "world"}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base_api.urls),
]
