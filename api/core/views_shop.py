import hashlib
import json
import random
import time

from django.core.handlers.wsgi import WSGIRequest
from django.db import reset_queries, connection
from django.db.models import Subquery
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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
        shop_reg_code = ShopMemberRegistrationCode.objects.get(code = code, used=False)
        shop_reg_code.used = True
        shop_reg_code.save()
        shop_id = shop_reg_code.shop.id
        user = TelegramUser.objects.get(telegram_id=user_id)
        ShopMember.objects.create(user=user, shop_id=shop_id)
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
        shop = Shop.objects.get(id=shop_id)

        available_models = shop.available_models.values('id')
        parts = shop.parts.values('id')


        black_list = ShopOrdersBlacklist.objects.filter(shop_id=shop_id)


        orders = Order.objects.filter(
            status=OrderStatus.PENDING,
            model_id__in=available_models,
            part_id__in=parts,
        ).exclude(id__in=black_list.values('order'))

        black_list = OrderOffer.objects.filter(shop_id=shop_id)

        orders = orders.exclude(id__in=black_list.values('order'))


        available_orders_cnt = len(orders)
        if available_orders_cnt <= skip:
            return JsonResponse({'cnt': available_orders_cnt, 'data':[]}, safe=False)
        limit = min(skip + limit, len(orders))

        orders = sorted(
            orders,
            key=lambda x: x.model.__str__(),
        )

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
        orders = Order.objects.order_by('model').filter(
            status=OrderStatus.ACTIVE,
            offer__shop_id=shop_id,
        )
        active_orders_cnt = len(orders)
        if active_orders_cnt <= skip:
            return JsonResponse({'cnt': active_orders_cnt, 'data': []})



        limit = min(skip + limit, active_orders_cnt)

        orders = orders[skip:limit]

        res = {'cnt': active_orders_cnt, 'data': []}

        for i in orders:
            res['data'].append({
                'id': i.id,
                'title': f'Id: {i.id}, {i.model}, Price: {i.offer.price} DH',
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
                'title': f'Id: {i.id}, {i.model}, Price: {i.offer.price} DH, ',
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
            lat=request.POST['lat'],
            lon=request.POST['lon'],
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
            'lon': shop.lon,
            'lat': shop.lat,
        })


    def post(self, request, shop_id):
        shop = Shop.objects.get(id=shop_id)
        if 'name' in request.POST:
            shop.name = request.POST['name']

        if 'location' in request.POST:
            shop.location = request.POST['location']

        if 'phone' in request.POST:
            shop.phone = request.POST['phone']
        if 'lat' in request.POST:
            shop.lat = request.POST['lat']

        if 'lon' in request.POST:
            shop.lon = request.POST['lon']

        shop.save()
        return JsonResponse({'status': 'success'})

class AvailableBrands(APIView):
    def get(self, request, shop_id,skip, limit):
        shop = Shop.objects.get(id=shop_id)

        brands = CarBrand.objects.all().order_by('name')

        cnt = len(brands)

        if cnt <= skip:
            return JsonResponse({'cnt': cnt, 'data': []})
        limit = min(skip + limit, cnt)

        brands = brands[skip:limit]

        data = []

        for i in brands:
            prefix = '❌'
            if shop.available_models.filter(brand=i).exists():
                prefix = '✅'
            data.append({
                'id': i.id,
                'title': f'{prefix} {i.name}',
            })
        return JsonResponse({'cnt': cnt, 'data': data})



class MyOffers(APIView):
    def get(self, request, shop_id,skip, limit):
        offers = OrderOffer.objects.filter(shop_id=shop_id, order__status=OrderStatus.PENDING)

        cnt = len(offers)

        if cnt <= skip:
            return JsonResponse({'cnt': cnt, 'data': []})
        limit = min(skip + limit, cnt)

        brands = offers[skip:limit]

        data = []

        for i in brands:
            order = i.order
            data.append({
                'id': order.id,
                'title': f'Price:{i.price} Model: {order.model}',
            })
        return JsonResponse({'cnt': cnt, 'data': data})

class OfferInfo(APIView):
    def get(self, request,shop_id, order_id):
        offer = OrderOffer.objects.get(shop_id=shop_id, order_id=order_id)

        return JsonResponse(
            {
                'price': offer.price,
            }
        )

class CancelOffer(APIView):
    def post(self, request,shop_id, order_id):
        OrderOffer.objects.filter(shop_id=shop_id, order_id=order_id).delete()
        return JsonResponse(
            {
                'status': 'Ok.',
            }
        )


class ChangeOfferPrice(APIView):
    def post(self, request, shop_id, order_id):
        price = request.POST['price']
        offer = OrderOffer.objects.get(shop_id=shop_id, order_id=order_id)
        offer.price = price
        offer.save()
        return JsonResponse(
            {
                'status': 'Ok.',
            }
        )
class Models(APIView):
    def get(self, request, shop_id, brand_id,limit, skip, ):
        models = CarModel.objects.filter(brand__id = brand_id).order_by('name')

        cnt = len(models)
        if cnt <= skip:
            return JsonResponse({'cnt': cnt, 'data':[]})

        limit = min(skip+limit, cnt)

        models = models[skip:limit]

        shop = Shop.objects.get(id=shop_id)
        data = []
        for i in models:
            if shop.available_models.filter(id=i.id).exists():
                callback_data = f'shop_info_pick_model_{i.id}_0'
                title = f'✅ {str(i)}'
            else:
                callback_data = f'shop_info_pick_model_{i.id}_1'
                title = f'❌ {str(i)}'

            data.append({
                'title': title,
                'callback_data': callback_data,
                'id': i.id,
            })
        return JsonResponse({'cnt': cnt, 'data': data})


class PickModels(APIView):
    def post(self, request, shop_id):
        type = request.POST['type']
        shop = Shop.objects.get(id=shop_id)
        if type == 'all':
            brand_id = request.POST['brand_id']
            models = CarModel.objects.filter(brand_id=brand_id)
            status = request.POST['status']
            if status == '1':
                shop.available_models.add(*models)
            else:
                shop.available_models.remove(*models)
        if type == 'specify':
            data = request.POST.getlist('data')
            for i in data:
                json_acceptable_string = i.replace("'", "\"")
                i = json.loads(json_acceptable_string)
                model_id = i['model_id']
                status = i['status']
                try:
                    model = CarModel.objects.get(id=model_id)
                    if status == '1':
                        shop.available_models.add(model)
                    else:
                        shop.available_models.remove(model)
                except Exception as e:
                    print(e)
                    pass

        return JsonResponse({'status': 'success'})

class ShopMemberCodeCreation(APIView):
    def get(self, request, shop_id):
        code = str(time.time())
        code += str(random.randint(10, 100000000) * random.randint(10, 100000000) / random.randint(10, 100000000))
        code = hashlib.sha256(code.encode()).hexdigest()[:20]
        new_code = ShopMemberRegistrationCode(code=code, shop_id=shop_id)
        new_code.save()
        return JsonResponse({'code': new_code.code})

class PartTypeView(APIView):
    def get(self, request, shop_id):


        shop = Shop.objects.get(id=shop_id)

        available_part_types = PartType.objects.all()


        res = []
        for part in available_part_types:




            if shop.parts.filter(id=part.id).exists():
                callback_data = f'shop_info_pick_part_{part.id}_0'
                title = f'✅ {part.name}'
            else:
                callback_data = f'shop_info_pick_part_{part.id}_1'
                title = f'❌ {part.name}'
            res.append(
                {
                    'title': title,
                    'callback_data': callback_data,
                }
            )

        return JsonResponse({'status': 'OK', 'data': res})



    def post(self, request, shop_id):
        part_id = request.POST['part_id']
        part_status = request.POST['status']

        shop = Shop.objects.get(id=shop_id)
        part = PartType.objects.get(id=part_id)


        if part_status == '1':
            shop.parts.add(part)
        else:
            shop.parts.remove(part)
        shop.save()

        shop = Shop.objects.get(id=shop_id)

        return JsonResponse({'status': 'success'})

def create_test_brands(self):
    for i in range(45, 0, -1):
        brand = CarBrand(name=f'Brand name {i}testing')
        brand.save()


