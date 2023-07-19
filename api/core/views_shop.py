from django.core.handlers.wsgi import WSGIRequest
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
    ShopMember.object.create(user__telegram_id=tg_id, shop__id=shop_id)


class CreateShop(APIView):
    def post(self, request: WSGIRequest):
        tg_id = request.POST['tg_id']
        del request.path['tg_id']
        obj = Shop.objects.create(**request.POST)
        create_shop_member(obj.id, tg_id)
        return JsonResponse({'status':'success'}, status=200)

