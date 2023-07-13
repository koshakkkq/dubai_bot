from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("get_car_brands/", views.CarBrandApiView.as_view()),
]