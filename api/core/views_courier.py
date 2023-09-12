import hashlib
import json
import logging
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

logger = logging.getLogger(__name__)


class CourierStatus(APIView):
    def get(self, request: WSGIRequest, user_id):
        try:
            TelegramUser.objects.get(~Q(courier=None), telegram_id=user_id)
            return JsonResponse({'status': 'courier'})
        except TelegramUser.DoesNotExist:
            pass

        try:
            return JsonResponse({'status': 'can_be_courier'})
        except CourierRegistrationCode.DoesNotExist:
            pass
        return JsonResponse({'status': 'register'})


class CheckCourierCode(APIView):
    def get(self, request, user_id, code):
        # try:
        #     code = CourierRegistrationCode.objects.get(code=code, used=False)
        #     code.used = True
        #     code.user = user_id
        #     code.save()
        #     return JsonResponse({'status': True})
        # except TelegramUser.DoesNotExist:
        #     return JsonResponse({'status': False})
        #     pass
        return JsonResponse({'status': True})

class CreateCourier(APIView):

    def post(self, request):
        tg_id = request.POST['user_id']
        phone = request.POST['phone']
        name = request.POST['name']

        courier = Courier.objects.create(phone=phone, name=name)

        user = TelegramUser.objects.get(telegram_id=tg_id)

        user.courier = courier

        user.save()

        return JsonResponse({'Success': True})


class CourierInfo(APIView):
    def get(self, request, tg_id):
        try:
            user = TelegramUser.objects.get(telegram_id=tg_id)
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


class AvailableOrders(APIView):
    def get(self, request, courier_id, skip, limit):

        user = TelegramUser.objects.get(courier_id=courier_id)

        blacklist = CourierOrdersBlacklist.objects.filter(user=user).values('order')

        courier_offer_blacklist = CourierOffer.objects.filter(courier_id=courier_id).values('order')

        orders = Order.objects.filter(credential__courier_offer=None, status=OrderStatus.ACTIVE,
                                      credential__is_delivery=True,
                                      ).exclude(id__in=blacklist).exclude(id__in=courier_offer_blacklist)

        orders_cnt = len(orders)
        if orders_cnt <= skip:
            return JsonResponse({'cnt': orders_cnt, 'data': []}, safe=False)

        orders = sorted(
            orders,
            key=lambda x: x.model.__str__(),
        )

        limit = min(skip + limit, len(orders))

        orders = orders[skip:limit]

        res = {'cnt': orders_cnt, 'data': []}
        for i in orders:
            res['data'].append({
                'id': i.id,
                'title': f'Id: {i.id}, {i.model.__str__()}  ',
            })

        return JsonResponse(res)


class OrderInfo(APIView):
    def get(self, request, order_id):
        return JsonResponse({'status': True, 'data': self.get_order_info(order_id)})

    @staticmethod
    def get_order_info(order_id):
        order = Order.objects.get(id=order_id)

        status = ''
        for i in OrderStatus.__dict__:
            if OrderStatus.__dict__[i] == order.status:
                status = i
                break

        phone = order.credential.phone

        if phone == None:
            phone = '-'

        return {
            'id': order.id,
            'shop_address': order.offer.shop.location,
            'client_address': order.credential.address,
            'tg_id': order.customer.telegram_id,
            'status': status,
            'client_phone': phone,
            'shop_phone': order.offer.shop.phone,
            'price': order.offer.price,
            'additional': order.additional,
            'shop_lat': order.offer.shop.lat,
            'shop_lon': order.offer.shop.lon,
            'cred_lat': order.credential.lat,
            'cred_lon': order.credential.lon,
        }

    def post(self, request, order_id):
        try:

            order_data = self.get_order_info(order_id)
            courier_id = request.POST['courier_id']

            order = Order.objects.get(id=order_id, credential__courier=None, status=OrderStatus.ACTIVE)

            courier = Courier.objects.get(id=courier_id)

            order.credential.courier = courier

            order.credential.save()

            return JsonResponse({'status': True, 'data': order_data})
        except Exception as e:
            logging.error(e)
            return JsonResponse({'status': False})


class AddOrderToCourierBlacklist(APIView):
    def get(self, request, order_id, courier_id):
        user = TelegramUser.objects.get(courier_id=courier_id)

        CourierOrdersBlacklist.objects.create(user=user, order_id=order_id)

        return JsonResponse({'status': False})


class CouriersOrders(APIView):
    def get(self, request, courier_id, status, skip, limit):
        if status == OrderStatus.ACTIVE:
            statuses = [OrderStatus.ACTIVE]
        else:
            statuses = [OrderStatus.DONE, OrderStatus.CANCELED]

        orders = Order.objects.filter(status__in=statuses, credential__courier_offer__courier_id=courier_id).order_by(
            'id')

        orders_cnt = len(orders)
        if orders_cnt <= skip:
            return JsonResponse({'cnt': orders_cnt, 'data': []}, safe=False)

        limit = min(skip + limit, len(orders))

        orders = orders[skip:limit]

        data = []

        for i in orders:
            data.append({
                'id': i.id,
                'title': f'Id: {i.id}, {i.model.__str__()}',
            })

        return JsonResponse({'cnt': orders_cnt, 'data': data})


class CourierOfferView(APIView):
    def post(self, request, courier_id):
        order_id = request.POST['order_id']
        price = request.POST['price']

        CourierOffer.objects.create(
            courier_id=courier_id,
            order_id=order_id,
            price=price,
        )

        return JsonResponse({'status': 'Success'})


class CourierFeedbackView(APIView):
    def post(self, request):
        order_id = request.POST['order_id']
        mark = request.POST['mark']
        comment = request.POST['comment']

        order = Order.objects.get(id=order_id)

        courier = order.credential.courier

        CourierFeedback.objects.create(comment=comment, rating=mark, courier=courier)

        return JsonResponse({'status': 'Ok.'})
