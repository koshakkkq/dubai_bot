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
from .resources import CarModelResource

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.

@admin.register(ShopMemberRegistrationCode)
class ShopMemberRegistrationCode(admin.ModelAdmin):
    list_display = ('code', 'used', 'shop', 'creation_time',)
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


    list_display = ('id', 'code', 'used', 'user', 'get_time',)
    change_list_template = 'admin/core/shopregistrationcode/change_list.html'
    get_time.admin_order_field = 'creation_time'
    ordering = ('-id', )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id','telegram_id','get_courier')
    sortable_by = (
        "id",
        "telegram_id",
    )

    @admin.display(description='Courier')
    def get_courier(self, obj: TelegramUser):
        return obj.courier

    get_courier.admin_order_field = 'Courier'
    get_courier.empty_value_display = 'Not a courier'


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')

@admin.register(CourierFeedback)
class CourierFeedbackAdmin(admin.ModelAdmin):
    list_display = ('comment', 'rating', 'courier')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'phone')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['available_models'].widget.can_add_related = False
        return form

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
@admin.register(ShopFeedback)
class ShopFeedbackAdmin( admin.ModelAdmin):
    list_display = ('comment', 'raiting', 'shop')


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(CarModel)
class CarModelAdmin(ImportExportModelAdmin, ImportExportMixin, admin.ModelAdmin):
    resource_class = CarModelResource
    list_display = ('id','brand','name', 'internal_name',  'get_years', )

    @admin.display(description='years')
    def get_years(self, obj: CarModel):
        return f'{obj.production_start}-{obj.production_end}'


@admin.register(ShopMember)
class ShopMemberAdmin( admin.ModelAdmin):
    list_display = ('user', 'shop')

@admin.register(ShopOrdersBlacklist)#todo удалить для клиента
class ShopOrdersBlacklistAdmin(admin.ModelAdmin):
    list_display = ('shop', 'order')

@admin.register(CourierOrdersBlacklist)  # todo удалить для клиента
class CourierOrdersBlacklistAdmin(admin.ModelAdmin):
    list_display = ('user', 'order')

@admin.register(MessageToDelete)  # todo удалить для клиента
class MessageToDeleteAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_id', 'msg_id')

@admin.register(UserNotification)  # todo удалить для клиента
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'new_offers', 'new_couriers')


@admin.register(ShopNotification)  # todo удалить для клиента
class ShopNotificationAdmin(admin.ModelAdmin):
    list_display = ('shop', 'new_available_orders', 'new_active_orders')


@admin.register(OrderCredential)
class OrderCredential( admin.ModelAdmin):
    list_display = ('address', 'get_courier', 'is_delivery', 'phone')
    @admin.display(description='courier')
    def get_courier(self, obj):
        return obj.courier

    get_courier.admin_order_field = 'courier'
    get_courier.empty_value_display = 'Not a courier'


@admin.register(Order)
class OrderAdmin( admin.ModelAdmin):
    list_display = ('id','customer', 'credential', 'model', 'status', 'additional', 'get_time')

    @admin.display(description='Order creation')
    def get_time(self, obj):
        return obj.datetime.strftime("%d %b %Y %H:%M:%S")


    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)

        order = obj.offer

        blacklist = Order.objects.exclude(offer=None).values('offer_id')


        offers = OrderOffer.objects.exclude(id__in=blacklist)

        if order is not None:
            try:
                offer_query = OrderOffer.objects.filter(id=order.id)
                offers |= offer_query
            except Exception as e:
                pass
        form.base_fields['offer'].queryset = offers

        return form
@admin.register(OrderOffer)
class OrderOfferAdmin( admin.ModelAdmin):
    list_display = ('get_shop', 'price', 'order')

    @admin.display(description='shop')
    def get_shop(self, obj):
        return obj.shop.name


@admin.register(CourierRegistrationCode)
class CourierRegistrationCodeAdmin(admin.ModelAdmin):
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
        urls = super(CourierRegistrationCodeAdmin, self).get_urls()
        custom_urls = [
            re_path('^import/$', self.create_secret_code, name='process_import')
        ]
        return custom_urls+urls

    def create_secret_code(self, request):
        code = str(time.time())
        code += str(random.randint(10, 100000000) * random.randint(10, 100000000) / random.randint(10, 100000000))
        code = hashlib.sha256(code.encode()).hexdigest()[:20]
        new_code = CourierRegistrationCode(code=code)
        new_code.save()
        self.message_user(request, f"Created code: {new_code.code}")
        return HttpResponseRedirect("../")


    list_display = ('id','code', 'used', 'user', 'get_time',)
    change_list_template = 'admin/core/shopregistrationcode/change_list.html'
    get_time.admin_order_field = 'creation_time'
    ordering = ('-id', )


