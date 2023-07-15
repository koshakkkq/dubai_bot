from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import re_path
from django.urls import path

from .models import *

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

@admin.register(ShopRegistrationCode)
class ShopRegistrationCodeAdmin(admin.ModelAdmin):
    change_list_template = 'admin/core/shopregistrationcode/change_list.html'

    def get_urls(self):
        urls = super(ShopRegistrationCodeAdmin, self).get_urls()
        custom_urls = [
            re_path('^import/$', self.create_secret_code, name='process_import')
        ]
        return custom_urls+urls

    def create_secret_code(self, request):
        print(request.POST)
        self.message_user(request, f"создано {1} новых записей")
        return HttpResponseRedirect("../")