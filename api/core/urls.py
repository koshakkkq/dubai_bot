from django.urls import path
from core import views, views_shop

app_name = "core"

urlpatterns = [

    path("car_brands/", views.CarBrandApiView.as_view(), name="car_brands"),
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

    path("shop_member_status/<int:id>/", views_shop.shop_member_status),
    path('is_code_correct/<int:user_id>/<str:code>/', views_shop.is_code_correct),
    path('set_language/', views_shop.SetUserLanguage.as_view()),

    path('create_shop/', views_shop.CreateShop.as_view()),
    path('shop_available_orders/<int:shop_id>/<int:skip>/<int:limit>/', views_shop.AvailableOrders.as_view()),
    path('shop_active_orders/<int:shop_id>/<int:skip>/<int:limit>/', views_shop.ActiveOrders.as_view()),
    path('shop_order_info/<int:order_id>/', views_shop.OrderInfo.as_view()),
    path('shop_create_order_offer/', views_shop.CreateOrderOffer.as_view()),
    path('shop_add_order_blacklist/', views_shop.AddShopOrderToBlackList.as_view()),
]