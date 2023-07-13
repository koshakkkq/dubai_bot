from django.contrib import admin
from .models import CourierFeedback, ShopFeedback, Courier, TelegramUser, CarBrand, CarModel, Shop, ShopMember, OrderCredential, Order, OrderOffer

# Register your models here.
admin.site.register(CourierFeedback)
admin.site.register(ShopFeedback)
admin.site.register(Courier)
admin.site.register(TelegramUser)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(Shop)
admin.site.register(ShopMember)
admin.site.register(OrderCredential)
admin.site.register(Order)
admin.site.register(OrderOffer)