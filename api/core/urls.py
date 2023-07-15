from django.urls import path
from core import views

app_name = "core"

urlpatterns = [

    path("car_brands/", views.CarBrandApiView.as_view()),
    path("courier/", views.CourierApiView.as_view()),
    path("courier_feedback/", views.CourierFeedbackApiView.as_view()),
    path("telegram_user/", views.TelegramUserApiView.as_view()),
    path("car_brand/", views.CarBrandApiView.as_view()),
    path("car_model/", views.CarModelApiView.as_view()),
    path("shop/", views.ShopApiView.as_view()),
    path("shop_feedback/", views.ShopFeedbackApiView.as_view()),
    path("shop_member/", views.ShopMemberApiView.as_view()),
    path("order_credentials/", views.OrderCredentialApiView.as_view()),
    path("order/", views.OrderApiView.as_view()),
    path("order_offer/", views.OrderOfferApiView.as_view()),

]