from django.db.models.signals import post_delete, post_migrate
from django.dispatch import receiver
from .models import *
from .constants import part_types
@receiver(post_delete, sender=TelegramUser)
def wrapper(sender, instance: TelegramUser, *args, **kwargs):
	tg_id = instance.telegram_id
	CourierRegistrationCode.objects.filter(user=tg_id).delete()
	ShopRegistrationCode.objects.filter(user=tg_id).delete()

@receiver(post_delete, sender=ShopMember)
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
				ShopNotification.objects.filter(
					shop=instance.offer.shop,
				).update(new_active_orders=F('new_active_orders') + 1)
	except Order.DoesNotExist:
		model = instance.model
		part = instance.part
		shops_with_order_model = Shop.objects.filter(available_models=model, parts=part)
		notifications = ShopNotification.objects.filter(shop__in=shops_with_order_model)
		notifications.update(new_available_orders=F('new_available_orders') + 1)
	except Exception as e:
		pass


# @receiver(pre_save, sender=OrderCredential)
# def wrapper(sender, instance: OrderCredential, raw, update_fields, *args, **kwargs):
# 	try:
# 		instance_in_db = OrderCredential.objects.get(id=instance.pk)
# 		if instance_in_db.courier is None and instance.courier is not None:
# 			order = instance.order
# 			user = order.customer
# 			UserNotification.objects.filter(user=user).update(
# 				new_couriers=F('new_couriers') + 1
# 			)
# 	except OrderCredential.DoesNotExist:
# 		pass
# 	except Exception as e:
# 		print(e)
# 		pass


@receiver(pre_save, sender=CourierOffer)
def wrapper(sender, instance: CourierOffer, raw, update_fields, *args, **kwargs):
	user = instance.order.customer

	UserNotification.objects.filter(user=user).update(
	 				new_couriers=F('new_couriers') + 1
				)

def run_post_migrate(sender, **kwargs):
	for id, name in enumerate(part_types):
		try:
			PartType.objects.get(name=name)
		except Exception:
			PartType.objects.create(pk=id+1, name=name)
