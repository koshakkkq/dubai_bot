from rest_framework import serializers
from core.models import *


class CarBrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ["id", "name", "models"]


class CarBrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ["id", "name", "models"]
        depth = 2


class CarModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ["id", "name", "internal_name", "years", "brand"]


class CarModelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ["id", "name", "internal_name", "years", "brand"]
        depth = 2


class CourierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ["id", "name", "phone", "feedbacks", "telegram_user"]


class CourierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ["id", "name", "phone", "feedbacks", "telegram_user"]
        depth = 2


class TelegramUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ["id", "telegram_id", "language", "courier", "member", "orders"]


class TelegramUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ["id", "telegram_id", "language", "courier", "member", "orders"]
        depth = 2


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "location", "phone", "available_models", "feedbacks", "members", "offers"]


class ShopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "location", "phone", "available_models", "feedbacks", "members", "offers"]
        depth = 2


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "product", "additional", "datetime", "customer", "credential", "model", "offers"]
        depth = 2


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "product", "additional", "datetime", "customer", "credential", "model", "offers"]
        depth = 2


class OrderOfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOffer
        fields = '__all__'


class OrderOfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOffer
        fields = '__all__'
        depth = 2