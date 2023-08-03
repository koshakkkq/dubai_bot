from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.utils.timezone import now

from core.models import CarBrand
from core.serializers import *
from .models import *
from .mixins import *
import json
from .constants import VERBOSE_ORDER_TYPE


class CourierApiView(APIView, DataMixin):
    serializer_class = CourierSerializer
    model = Courier


class CourierFeedbackApiView(APIView, DataMixin):
    serializer_class = CourierFeedbackSerializer
    model = CourierFeedback


class TelegramUserApiView(APIView, DataMixin):
    serializer_class = TelegramUserSerializer
    model = TelegramUser


class CarBrandApiView(APIView, DataMixin):
    serializer_class = CarBrandSerializer
    model = CarBrand


class CarModelApiView(APIView, DataMixin):
    serializer_class = CarModelSerializer
    model = CarModel


class ShopApiView(APIView, DataMixin):
    serializer_class = ShopSerializer
    model = Shop


class ShopFeedbackApiView(APIView, DataMixin):
    serializer_class = ShopFeedbackSerializer
    model = ShopFeedback


class ShopMemberApiView(APIView, DataMixin):
    serializer_class = ShopMemberSerializer
    model = ShopMember


class OrderCredentialApiView(APIView, DataMixin):
    serializer_class = OrderCredentialSerializer
    model = OrderCredential


class OrderApiView(APIView, DataMixin):
    serializer_class = OrderSerializer
    model = Order


class OrderOfferApiView(APIView, DataMixin):
    serializer_class = OrderOfferSerializer
    model = OrderOffer


class OrderDetailApiView(APIView):
    serializer_class = OrderSerializer
    model = Order

    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
            serializer = self.serializer_class(order).data
            return Response(serializer, status=200)
        except Exception as e:
            print(e)
        return JsonResponse({})


class OrderCreateApiView(APIView):
    def post(self, request: WSGIRequest):
        telegram_user_id = request.POST.get("telegram_user_id")
        additional = request.POST.get("additional")
        model_id = request.POST.get("model_id")
        part_name = request.POST.get('part_name')
        part = PartType.objects.get(name=part_name)


        telegram_user = TelegramUser.objects.get(telegram_id=telegram_user_id)
        model = CarModel.objects.get(id=model_id)
        order = Order.objects.create(customer=telegram_user, model=model, additional=additional, part=part)
        return JsonResponse({'status':'success'}, status=200)


class ExtendedOrderApiView(OrderApiView):
    def post(self, request):
        try:
            status = request.POST.get("status")
            telegram_user_id = request.POST.get("telegram_user_id")
            telegram_user = TelegramUser.objects.get(telegram_id=telegram_user_id)
            orders = Order.objects.filter(customer=telegram_user, status=status)
            data = []
            for order in orders:
                lst = []
                for offer in order.offers.all():
                    shop = offer.shop
                    feedback = ShopFeedback.objects.filter(shop=shop)
                    if len(feedback.all()) == 0:
                        raiting = 0
                    else:
                        raiting = sum(feedback.values_list("raiting", flat=True)) / len(feedback.all())
                    lst.append({"raiting": raiting, "id": offer.id, "price": offer.price, "shop":
                        {"id": shop.id, "name": shop.name, "location": shop.location, "phone": shop.phone}})



                delta = {"id": order.id, "status": {"id": order.status, "name": VERBOSE_ORDER_TYPE[order.status]},
                         "offers": lst, "model": str(order.model), "additional": order.additional,
                         }
                if int(status) > 0:
                    delta["offer"] = OrderOfferSerializer(order.offer).data
                data.append(delta)
            return JsonResponse(data, status=200, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse([])


class OrderUpdateApiView(APIView):
    def post(self, request):
        try:
            order_id = request.POST.get("order_id")
            offer_id = request.POST.get("offer_id")
            is_delivery = request.POST.get("is_delivery")
            address = request.POST.get("address")
            status = request.POST.get("status")
            lat = request.POST.get("lat")
            lon = request.POST.get("lon")

            order = Order.objects.get(id=order_id)
            order.offer_id = offer_id
            order.status = status
            order.credential = OrderCredential.objects.create(address=address, is_delivery=is_delivery, lat=lat, lon=lon)
            order.datetime = now()
            order.save()
            return JsonResponse({'status':'success'}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error"})


class MsgToDeleteView(APIView):
    def get(self, request, tg_id):
        try:
            msg = MessageToDelete.objects.get(tg_id=tg_id)
            msg_id = msg.msg_id
            msg.msg_id = None
            msg.save()
            return JsonResponse({'msg': msg_id})
        except Exception :
            return JsonResponse({'msg': None})

    def post(self, request,tg_id):
        msg_id = request.POST['msg_id']
        msg = MessageToDelete.objects.get_or_create(
            tg_id=tg_id,
        )
        msg[0].msg_id = msg_id
        msg[0].save()
        return JsonResponse({'msg':None}, status=200)


class ShopFeedbackCreateApiView(APIView):
    def post(self, request):
        try:
            shop_id = request.POST.get("shop_id")
            mark = request.POST.get("mark")
            comment = request.POST.get("comment")
            feedback = ShopFeedback.objects.create(shop_id=shop_id, raiting=int(mark), comment=comment)
            feedback.save()
            return JsonResponse({'status':'success'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error"})


class NotificationsView(APIView):
    def get(self, request):
        res = {
            'status': 'Success',
            'data': []
        }
        all_notifications = []
        shop_notifications = ShopNotification.objects.filter(Q(new_available_orders__gt=0) | Q(new_active_orders__gt=0))


        shop_notifications = shop_notifications[:min(len(shop_notifications) + 1, 10)]


        for notification in shop_notifications:
            if len(all_notifications) >= 10:
                break
            shop_members = ShopMember.objects.filter(shop=notification.shop)

            for member in shop_members:
                all_notifications.append(
                    {
                        'type': 'shop',
                        'user_id': member.user.telegram_id,
                        'new_available_orders': notification.new_available_orders,
                        'new_active_orders': notification.new_active_orders,
                    }
                )
            notification.new_available_orders = F('new_available_orders') - notification.new_available_orders
            notification.new_active_orders = F('new_active_orders') - notification.new_active_orders
            notification.save()


        user_notifications = UserNotification.objects.filter(Q(new_offers__gt=0) | Q(new_couriers__gt=0))

        user_notifications = user_notifications[:min(len(user_notifications) + 1, 10)]

        for notification in user_notifications:
            if len(all_notifications) >= 10:
                break
            all_notifications.append(
                {
                    'type': 'user',
                    'user_id': notification.user.telegram_id,
                    'new_offers': notification.new_offers,
                    'new_couriers': notification.new_couriers,
                }
            )
            notification.new_offers = F('new_offers') - notification.new_offers
            notification.new_couriers = F('new_couriers') - notification.new_couriers
            notification.save()
        res['data'] = all_notifications
        return JsonResponse(res)



class ResetUserNotifications(APIView):
    def post(self, request):
        try:
            tg_id = request.POST['tg_id']
            user = TelegramUser.objects.get(telegram_id=tg_id)
            user_notification = UserNotification.objects.get(user = user)
            if 'new_offers' in request.POST:
                user_notification.new_offers = 0
            if 'new_couriers' in request.POST:
                user_notification.new_couriers = 0
            user_notification.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False})

class ResetShopNotifications(APIView):
    def post(self, request):
        try:
            shop_id = request.POST['shop_id']
            shop_notification = ShopNotification.objects.get(shop_id=shop_id)
            if 'new_available_orders' in request.POST:
                shop_notification.new_available_orders = 0
            if 'new_active_orders' in request.POST:
                shop_notification.new_active_orders = 0
            shop_notification.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False})


def order_increase(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = order.status + 1
    order.save()
    return JsonResponse({})