from rest_framework import serializers
from core.models import CarBrand


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ("id", "name")