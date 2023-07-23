import hashlib
import json
import random
import time

from django.core.handlers.wsgi import WSGIRequest
from django.db import reset_queries, connection
from django.db.models import Subquery
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .models import *
from .constants import OrderStatus
from django.db.models import Q


class CourierStatus(APIView):
    def get(self, request: WSGIRequest, user_id):
        try:
            TelegramUser.objects.get(~Q(courier=None),telegram_id=user_id)
            return JsonResponse({'status':'courier'})
        except TelegramUser.DoesNotExist:
            pass

        try:
            CourierRegistrationCode.objects.get(user=user_id)
            return JsonResponse({'status':'can_be_courier'})
        except CourierRegistrationCode.DoesNotExist:
            pass
        return JsonResponse({'status':'register'})


class CheckCourierCode(APIView):
    def get(self, request, user_id, code):
        try:
            code = CourierRegistrationCode.objects.get(code=code, used=False)
            code.used = True
            code.user = user_id
            code.save()
            return JsonResponse({'status': True})
        except TelegramUser.DoesNotExist:
            return JsonResponse({'status': False})
            pass

class CreateCourier(APIView):

    def post(self, request):
        tg_id = request.POST['user_id']
        phone = request.POST['phone']
        name = request.POST['name']

        courier = Courier.objects.create(phone=phone, name=name)

        user = TelegramUser.objects.get(telegram_id = tg_id)

        user.courier = courier

        user.save()

        return JsonResponse({'Success': True})

class CourierInfo(APIView):
    def get(self, request, tg_id):
        try:
            user = TelegramUser.objects.get(telegram_id = tg_id)
            courier_id = user.courier.id
            phone = user.courier.phone
            name = user.courier.name
            return JsonResponse({
                'courier_id': courier_id,
                'phone': phone,
                'name': name,
            })
        except Exception as e:
            return JsonResponse({})

    def post(self, request, tg_id):
        courier = Courier.objects.get(id=tg_id)

        field = request.POST['field']
        value = request.POST['value']

        courier.__dict__[field] = value
        courier.save()

        return JsonResponse({})