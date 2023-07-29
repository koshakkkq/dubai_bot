from django.dispatch import receiver
from .models import *

@receiver(pre_delete, sender=TelegramUser)
def wrapper(sender, instance: TelegramUser, *args, **kwargs):
	tg_id = instance.telegram_id
	CourierRegistrationCode.objects.filter(user=tg_id).delete()
	ShopRegistrationCode.objects.filter(user=tg_id).delete()

@receiver(pre_delete, sender=ShopMember)
def wrapper(sender, instance: ShopMember, *args, **kwargs):
	tg_id = instance.user.telegram_id
	ShopRegistrationCode.objects.filter(user=tg_id).delete()

@receiver(post_save, sender=Shop)
def wrapper(sender, instance: Shop, raw, update_fields, *args, **kwargs):
	if kwargs['created'] is True:
		ShopNotification.objects.create(shop=instance)


@receiver(post_save, sender=TelegramUser)
def wrapper(sender, instance, raw, update_fields, *args, **kwargs):
	if kwargs['created'] is True:
		UserNotification.objects.create(user=instance)

@receiver(post_save, sender=OrderOffer)
def wrapper(sender, instance: OrderOffer, raw, update_fields, *args, **kwargs):
	user = instance.order.customer
	if raw == False and instance.order.offer is None:
		UserNotification.objects.filter(user=user).update(new_offers= F('new_offers') + 1)


@receiver(pre_save, sender=Order)
def wrapper(sender, instance: Order, raw, update_fields, *args, **kwargs):
	try:
		instance_in_db = Order.objects.get(id=instance.pk)
		if instance_in_db.status == OrderStatus.PENDING and instance.status == OrderStatus.ACTIVE:
			if instance.offer is not None:
				ShopNotification.objects.update_or_create(
					shop=instance.offer.shop,
					defaults={
						'new_active_orders': F('new_active_orders') + 1
					}
				)
	except Order.DoesNotExist:
		model = instance.model
		shops_with_order_model = Shop.objects.filter(available_models=model)
		notifications = ShopNotification.objects.filter(shop__in=shops_with_order_model)
		notifications.update(new_available_orders=F('new_available_orders') + 1)
