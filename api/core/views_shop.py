import json

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Subquery
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .models import *
def shop_member_status(request: WSGIRequest, id):

    shop_member = ShopMember.objects.filter(user__telegram_id=id)
    if len(shop_member) != 0:
        return JsonResponse({'status': 'member'})

    shop_registration_code = ShopRegistrationCode.objects.filter(user=id,used=True)
    if len(shop_registration_code) != 0:
        return JsonResponse({'status': 'can_create_shop'})

    return JsonResponse({'status':'not_member'})

def is_code_correct(request: WSGIRequest, user_id, code):
    try:
        reg_code = ShopRegistrationCode.objects.get(code=code, used=False)
        reg_code.user = user_id
        reg_code.used = True
        reg_code.save()
        return JsonResponse({'status': True})
    except ShopRegistrationCode.DoesNotExist:
        pass


    try:
        shop_reg_code = ShopMemberRegistrationCode(code = code, used=False)
        shop_reg_code.used = True
        shop_reg_code.save()
        shop_id = shop_reg_code.shop.id
        ShopMember.objects.create(user_telegram_id=user_id, shop_id=shop_id)
        return JsonResponse({'status': True})
    except ShopMemberRegistrationCode.DoesNotExist:
        pass

    return JsonResponse({'status': False})


class SetUserLanguage(APIView):
    def post(self, request: WSGIRequest):
        tg_id = request.POST.get('tg_id')
        lanugage = request.POST.get('language')
        obj = TelegramUser.objects.get_or_create(telegram_id=tg_id)[0]
        obj.language = lanugage
        obj.save()
        return JsonResponse({'status':'success'}, status=200)

def create_shop_member(shop_id, tg_id):
    obj = TelegramUser.objects.get(telegram_id=tg_id)
    ShopMember.objects.create(user=obj, shop_id=shop_id)


class AvailableOrders(APIView):
    def get(self, request: WSGIRequest, shop_id, skip, limit):
        black_list = ShopOrdersBlacklist.objects.filter(shop_id=shop_id)
        orders = Order.objects.order_by('model').filter(status=1).exclude(id__in=black_list.values('order'))
        black_list = OrderOffer.objects.filter(shop_id=shop_id)
        orders = orders.exclude(id__in=black_list.values('order'))
        available_orders_cnt = len(orders)
        if len(orders) <= skip:
            return JsonResponse({'available_orders_cnt': available_orders_cnt, 'data':[]}, safe=False)
        limit = min(skip + limit, len(orders))
        orders = orders[skip:limit]
        res = {'available_orders_cnt':available_orders_cnt, 'data': []}
        for i in orders:
            res['data'].append({
                'id': i.id,
                'title': i.model.__str__(),
            })
        return JsonResponse(res)


class CreateShop(APIView):
    def post(self, request: WSGIRequest):
        tg_id = request.POST['tg_id']
        obj = Shop.objects.create(
            name=request.POST['name'],
            location=request.POST['location'],
            phone=request.POST['phone'],
        )
        create_shop_member(obj.id, tg_id)
        return JsonResponse({'status':'success'}, status=200)


class OrderInfo(APIView):

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'status': 'does_not_exist', 'data': {}})
            return
        res = {
            'id': order.id,
            'product': order.product,
            'model': str(order.model),
            'additional': order.additional,
        }

        return JsonResponse({'status':'order_info', 'data': res})


class CreateOrderOffer(APIView):

    def post(self, request: WSGIRequest):
        shop_id = request.POST.get('shop_id')
        order_id = request.POST.get('order_id')
        price = request.POST.get('price')

        OrderOffer.objects.create(shop_id=shop_id, order_id=order_id, price = price)

        return JsonResponse({'status':'success'}, status=200)

class AddShopOrderToBlackList(APIView):
    def post(self, request: WSGIRequest):
        shop_id = request.POST.get('shop_id')
        order_id = request.POST.get('order_id')

        ShopOrdersBlacklist.objects.create(shop_id=shop_id, order_id=order_id)

        return JsonResponse({'status':'success'}, status=200)