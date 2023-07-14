from rest_framework import generics
from rest_framework.views import APIView
from core.models import CarBrand
from core.serializers import *
from .models import *
from .mixins import DataListMixin, DataDetailMixin


class CarBrandListApiView(APIView, DataListMixin):
    serializer_class = CarBrandListSerializer
    model = CarBrand


class CarBrandDetailApiView(APIView, DataDetailMixin):
    serializer_class = CarBrandDetailSerializer
    model = CarBrand


class CarModelListApiView(APIView, DataListMixin):
    serializer_class = CarModelListSerializer
    model = CarModel


class CarModelDetailApiView(APIView, DataDetailMixin):
    serializer_class = CarModelDetailSerializer
    model = CarModel


class CourierListApiView(APIView, DataListMixin):
    serializer_class = CourierListSerializer
    model = Courier


class CourierDetailApiView(APIView, DataDetailMixin):
    serializer_class = CourierDetailSerializer
    model = Courier


class TelegramUserListApiView(APIView, DataListMixin):
    serializer_class = TelegramUserListSerializer
    model = TelegramUser


class TelegramUserDetailApiView(APIView, DataDetailMixin):
    serializer_class = TelegramUserDetailSerializer
    model = TelegramUser


class ShopListApiView(APIView, DataListMixin):
    serializer_class = ShopListSerializer
    model = Shop


class OrderListApiView(APIView, DataListMixin):
    serializer_class = OrderListSerializer
    model = Order


class OrderOfferListApiView(APIView, DataListMixin):
    serializer_class = OrderOfferListSerializer
    model = OrderOffer


class OrderOfferDetailApiView(APIView, DataDetailMixin):
    serializer_class = OrderOfferDetailSerializer
    model = OrderOffer