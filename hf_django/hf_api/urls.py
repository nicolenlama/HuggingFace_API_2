from django.urls import path

from . import views

urlpatterns = [
    path("api/search/v1/data.json", views.dataRequest, name="hf_api")
]
