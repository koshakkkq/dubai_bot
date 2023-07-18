import datetime
import hashlib
import random
import time

from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.http import HttpResponseRedirect
from django.urls import re_path
from django.urls import path
from import_export.admin import ImportExportMixin


from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import *

# Register your models here.


@admin.register(ShopRegistrationCode)
class ShopRegistrationCodeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    def get_actions(self, request):
        return {}


    @admin.display(description='Creation time')
    def get_time(self, obj: ShopRegistrationCode):
        return obj.creation_time.strftime("%d %b %Y %H:%M:%S")

    def get_urls(self):
        urls = super(ShopRegistrationCodeAdmin, self).get_urls()
        custom_urls = [
            re_path('^import/$', self.create_secret_code, name='process_import')
        ]
        return custom_urls+urls

    def create_secret_code(self, request):
        code = str(time.time())
        code += str(random.randint(10, 100000000) * random.randint(10, 100000000) / random.randint(10, 100000000))
        code = hashlib.sha256(code.encode()).hexdigest()[:20]
        new_code = ShopRegistrationCode(code=code)
        new_code.save()
        self.message_user(request, f"Created code: {new_code.code}")
        return HttpResponseRedirect("../")


    list_display = ('code', 'used', 'user', 'get_time',)
    change_list_template = 'admin/core/shopregistrationcode/change_list.html'
    get_time.admin_order_field = 'creation_time'
    ordering = ('creation_time', )


@admin.register(TelegramUser)
class TelegramUserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id','telegram_id','get_courier')

    @admin.display(description='Courier')
    def get_courier(self, obj: TelegramUser):
        return obj.courier

    get_courier.admin_order_field = 'Courier'
    get_courier.empty_value_display = 'Not a courier'


@admin.register(Courier)
class CourierAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'phone')

@admin.register(CourierFeedback)
class CourierFeedbackAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('comment', 'rating', 'courier')

@admin.register(Shop)
class ShopAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'phone')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['available_models'].widget.can_add_related = False
        return form

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
@admin.register(ShopFeedback)
class ShopFeedbackAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('comment', 'raiting', 'shop')


@admin.register(CarBrand)
class CarBrandAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(CarModel)
class CarBrandAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id','brand','name', 'internal_name',  'get_years', )

    @admin.display(description='years')
    def get_years(self, obj: CarModel):
        return f'{obj.production_start}-{obj.production_end}'


@admin.register(ShopMember)
class ShopMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user', 'shop')


@admin.register(OrderCredential)
class OrderCredential(ImportExportMixin, admin.ModelAdmin):
    list_display = ('address', 'get_courier', 'is_delivery', 'phone')
    @admin.display(description='courier')
    def get_courier(self, obj):
        return obj.courier

    get_courier.admin_order_field = 'courier'
    get_courier.empty_value_display = 'Not a courier'
@admin.register(Order)
class Order(ImportExportMixin, admin.ModelAdmin):
    list_display = ('customer', 'credential', 'model', 'status', 'product', 'additional', 'get_time')

    @admin.display(description='Order creation')
    def get_time(self, obj):
        return obj.datetime.strftime("%d %b %Y %H:%M:%S")

@admin.register(OrderOffer)
class OrderOfferAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('get_shop', 'price', 'get_order', 'order')

    @admin.display(description='shop')
    def get_shop(self, obj):
        return obj.shop.name

    @admin.display(description='order')
    def get_order(self, obj):
        return obj.order.product



