from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import CarBrand
from core.serializers import CarBrandSerializer


class CarBrandApiView(generics.ListAPIView):  # List of all car`s brands
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer