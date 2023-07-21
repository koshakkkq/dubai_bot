import json

from django.core.handlers.wsgi import WSGIRequest
from django.db import reset_queries, connection
from django.db.models import Subquery
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .models import *
from .constants import OrderStatus
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

        orders = Order.objects.order_by('model').filter(status=OrderStatus.PENDING).exclude(id__in=black_list.values('order'))

        black_list = OrderOffer.objects.filter(shop_id=shop_id)

        orders = orders.exclude(id__in=black_list.values('order'))

        available_orders_cnt = len(orders)
        if available_orders_cnt <= skip:
            return JsonResponse({'cnt': available_orders_cnt, 'data':[]}, safe=False)
        limit = min(skip + limit, len(orders))
        orders = orders[skip:limit]
        res = {'cnt':available_orders_cnt, 'data': []}
        for i in orders:
            res['data'].append({
                'id': i.id,
                'title': i.model.__str__(),
            })
        return JsonResponse(res)

class ActiveOrders(APIView):

    def get(self, request, shop_id, skip, limit):
        orders = Order.objects.order_by('model').filter(status=OrderStatus.ACTIVE, offer__shop_id=shop_id)
        active_orders_cnt = len(orders)
        if active_orders_cnt <= skip:
            return JsonResponse({'cnt': active_orders_cnt, 'data': []})



        limit = min(skip + limit, active_orders_cnt)

        orders = orders[skip:limit]

        res = {'cnt': active_orders_cnt, 'data': []}

        for i in orders:
            res['data'].append({
                'id': i.id,
                'title': f'{i.model}, Price: {i.offer.price} DH',
            })
        return JsonResponse(res)


class DoneOrders(APIView):

    def get(self, request, shop_id, skip, limit):
        orders = Order.objects.order_by('-id').filter(status__in=[OrderStatus.DONE, OrderStatus.CANCELED], offer__shop_id=shop_id)
        active_orders_cnt = len(orders)
        if active_orders_cnt <= skip:
            return JsonResponse({'cnt': active_orders_cnt, 'data': []})



        limit = min(skip + limit, active_orders_cnt)

        orders = orders[skip:limit]

        res = {'cnt': active_orders_cnt, 'data': []}

        for i in orders:
            res['data'].append({
                'id': i.id,
                'title': f'{i.model}, Price: {i.offer.price} DH, ',
            })
            if i.status == OrderStatus.DONE:
                res['data'][-1]['title'] += 'Status: done'
            else:
                res['data'][-1]['title'] += 'Status: cancel'
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
            'customer_id': order.customer.telegram_id,
        }
        for i in OrderStatus.__dict__:
            if OrderStatus.__dict__[i] == order.status:
                res['status'] = i

        if order.offer is not None:
            res['price'] = order.offer.price

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


class SetOrderStatus(APIView):
    def post(self, request):
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        if status == 'done':
            status = OrderStatus.DONE
        if status == 'cancel':
            status = OrderStatus.CANCELED

        order.status = status
        order.save()

        return JsonResponse({'status': 'success'})

class ShopInfo(APIView):
    def get(self, request, shop_id):
        shop = Shop.objects.get(id=shop_id)
        return JsonResponse({
            'name': shop.name,
            'location': shop.location,
            'phone': shop.phone,
        })


    def post(self, request, shop_id):
        shop = Shop.objects.get(id=shop_id)
        print(request.POST)
        if 'name' in request.POST:
            shop.name = request.POST['name']

        if 'location' in request.POST:
            shop.location = request.POST['location']

        if 'phone' in request.POST:
            shop.phone = request.POST['phone']

        shop.save()
        return JsonResponse({'status': 'success'})

class AvailableBrands(APIView):
    def get(self, request, skip, limit):
        brands = CarBrand.objects.all().order_by('name')
        cnt = len(brands)

        if cnt <= skip:
            return JsonResponse({'cnt': cnt, 'data': []})
        limit = min(skip + limit, cnt)

        brands = brands[skip:limit]

        data = []

        for i in brands:
            data.append({
                'id': i.id,
                'title': i.name,
            })

        return JsonResponse({'cnt': cnt, 'data': data})
def create_test_brands(self):
    for i in range(40, 0, -1):
        brand = CarBrand(name=f'Brand name {i}')
        brand.save()
