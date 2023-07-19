from rest_framework import generics
from rest_framework.views import APIView

from core.models import CarBrand
from core.serializers import *
from .models import *
from .mixins import *


class CourierApiView(APIView, DataMixin):
    serializer_class = CourierSerializer
    model = Courier


class CourierFeedbackApiView(APIView, DataMixin):
    serializer_class = CourierFeedbackSerializer
    model = CourierFeedback


class TelegramUserApiView(APIView, DataMixin):
    serializer_class = TelegramUserSerializer
    model = TelegramUser


class CarBrandApiView(APIView, DataMixin):
    serializer_class = CarBrandSerializer
    model = CarBrand


class CarModelApiView(APIView, DataMixin):
    serializer_class = CarModelSerializer
    model = CarModel


class ShopApiView(APIView, DataMixin):
    serializer_class = ShopSerializer
    model = Shop


class ShopFeedbackApiView(APIView, DataMixin):
    serializer_class = ShopFeedbackSerializer
    model = ShopFeedback


class ShopMemberApiView(APIView, DataMixin):
    serializer_class = ShopMemberSerializer
    model = ShopMember


class OrderCredentialApiView(APIView, DataMixin):
    serializer_class = OrderCredentialSerializer
    model = OrderCredential


class OrderApiView(APIView, DataMixin):
    serializer_class = OrderSerializer
    model = Order


class OrderOfferApiView(APIView, DataMixin):
    serializer_class = OrderOfferSerializer
    model = OrderOffer

