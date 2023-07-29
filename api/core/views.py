from django.core.handlers.wsgi import WSGIRequest
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

        telegram_user = TelegramUser.objects.get(telegram_id=telegram_user_id)
        model = CarModel.objects.get(id=model_id)
        order = Order.objects.create(customer=telegram_user, model=model, additional=additional)
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
                         "offers": lst, "model": str(order.model), "additional": order.additional}
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

            order = Order.objects.get(id=order_id)
            order.offer_id = offer_id
            order.status = status
            order.credential = OrderCredential.objects.create(address=address, is_delivery=is_delivery)
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


def order_increase(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = order.status + 1
    order.save()
    return JsonResponse({})