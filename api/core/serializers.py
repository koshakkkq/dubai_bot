from rest_framework import serializers
from core.models import *



class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('__all__')


class CourierFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierFeedback
        fields = ('__all__')


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('__all__')


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ('__all__')


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('__all__')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('__all__')


class ShopFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopFeedback
        fields = ('__all__')

class ShopMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ShopMember
        fields = ('__all__')


class OrderCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCredential
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('__all__')

class OrderOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOffer
        fields = ('__all__')

