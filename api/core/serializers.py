from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import *


class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ('__all__')


class CourierFeedbackSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(required=False, read_only=True)
    courier_id = serializers.PrimaryKeyRelatedField(queryset=Courier.objects.all(),source="courier",)

    class Meta:
        model = CourierFeedback
        fields = ('__all__')



class TelegramUserSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)
    courier_id = serializers.PrimaryKeyRelatedField(queryset=Courier.objects.all(), source="courier", required=False, default=None, write_only=True)

    class Meta:
        model = TelegramUser
        fields = ('__all__')


class CarBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        fields = ["id", "name", "models"]



class CarModelSerializer(serializers.ModelSerializer):
    brand = CarBrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=CarBrand.objects.all(), source="brand", write_only=True)
    class Meta:
        model = CarModel
        fields = ["id", "name", "internal_name",'production_start','production_end', "brand", 'brand_id']



class ShopSerializer(serializers.ModelSerializer):
    available_models = CarModelSerializer(many=True, read_only=True)
    available_models_id = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), source='available_models', many=True)
    class Meta:
        model = Shop
        fields = ["id", "name", "location", "phone", "available_models", "feedbacks", "members", "offers"]


class ShopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "location", "phone", "available_models", "feedbacks", "members", "offers"]
        depth = 2


class OrderDetailSerializer(serializers.ModelSerializer):
        model = ShopFeedback
        fields = ('__all__')


class ShopFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopFeedback
        fields = ('__all__')

class ShopMemberSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all(), source='user')

    #shop = ShopSerializer(read_only=True)
    #shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), source="shop")

    class Meta:
        model =  ShopMember
        fields = ('__all__')


class OrderCredentialSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)
    courier_id = serializers.PrimaryKeyRelatedField(queryset=Courier.objects.all(), source="courier")

    class Meta:
        model = OrderCredential
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):
    customer = TelegramUserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all(), source="customer", write_only=True)

    credential = OrderCredentialSerializer(read_only=True)
    credential_id = serializers.PrimaryKeyRelatedField(queryset=OrderCredential.objects.all(), source="credential", write_only=True)

    model_id = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), source="model", write_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "status", "additional", "datetime", "customer", "credential", "offer", "offers",
            'model_id','customer', 'credential', 'model', 'customer_id', 'credential_id', 'model_id',
        ]
        depth = 2


class OrderOfferSerializer(serializers.ModelSerializer):
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), source="shop", write_only=True)


    class Meta:
        model = OrderOffer
        fields = ('shop', 'shop_id', 'price', 'order')


