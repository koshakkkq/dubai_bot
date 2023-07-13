from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("car_brand/", views.CarBrandListApiView.as_view()),
    path("car_brand/<int:pk>/", views.CarBrandDetailApiView.as_view()),

    path("car_model/", views.CarModelListApiView.as_view()),
    path("car_model/<int:pk>/", views.CarModelDetailApiView.as_view()),

    path("courier/", views.CourierListApiView.as_view()),
    path("courier/<int:pk>/", views.CourierDetailApiView.as_view()),

    path("telegram_user/", views.TelegramUserListApiView.as_view()),
    path("telegram_user/<int:pk>/", views.TelegramUserDetailApiView.as_view()),

    path("shop/", views.ShopListApiView.as_view()),
    #path("shop/<int:pk>/", views.ShopApiView.as_view()),

    path("order/", views.OrderListApiView.as_view()),
    #path("order/<int:pk>/", views.OrderApiView.as_view()),

    path("order_offer/", views.OrderOfferListApiView.as_view()),
    path("order_offer/<int:pk>/", views.OrderOfferDetailApiView.as_view()),
]