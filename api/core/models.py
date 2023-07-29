import datetime

from django.db import models
from django.db.models import F
from django.db.models.signals import pre_delete, pre_save, post_save

from .constants import VERBOSE_ORDER_TYPE, VERBOSE_RAITING_TYPE, OrderStatus
from django.dispatch.dispatcher import receiver
class Courier(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)

	def __str__(self):
		return f'Name: {self.name}, Phone: {self.phone}'

	class Meta:
		verbose_name = "Courier"
		verbose_name_plural = "Couriers"


class CourierFeedback(models.Model):
	comment = models.TextField()
	rating = models.PositiveIntegerField(choices=VERBOSE_RAITING_TYPE, default=0)
	courier = models.ForeignKey(Courier, on_delete = models.CASCADE, related_name="feedbacks")


	def __str__(self):
		return f"{self.courier}|{self.rating}"

	class Meta:
		verbose_name = "Courier Feedback"
		verbose_name_plural = "Courier Feedbacks"


class TelegramUser(models.Model):
	telegram_id = models.BigIntegerField(db_index=True)
	language = models.CharField(max_length=40)
	courier = models.OneToOneField(Courier, on_delete = models.CASCADE, related_name="telegram_user", null=True, blank=True,
								   )

	def __str__(self):
		return f"Tg id: {self.telegram_id}"


	class Meta:
		verbose_name = "Telegram user"
		verbose_name_plural = "Telegram users"




class CarBrand(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Car brand"
		verbose_name_plural = "Car brands"


class CarModel(models.Model):
	brand = models.ForeignKey(CarBrand, on_delete = models.CASCADE, related_name="models")
	name = models.CharField(max_length=50)
	internal_name = models.CharField(max_length=50)
	production_start = models.PositiveIntegerField(default=0)
	production_end = models.PositiveIntegerField(default=0)
	#years = models.CharField(max_length=30)

	def __str__(self):
		return f"{self.brand} {self.name} {self.production_start}-{self.production_end}"

	class Meta:
		verbose_name = "Car model"
		verbose_name_plural = "Car models"

class ShopAvailableModels(models.Model):
	shop_id = models.ForeignKey


class Shop(models.Model):

	name = models.CharField(max_length=50)
	location = models.CharField(max_length=400)
	phone = models.CharField(max_length=100)
	available_models = models.ManyToManyField(CarModel, related_name="shops", )
	lat = models.FloatField(default=0)
	lon = models.FloatField(default=0)

	def __str__(self):
		return f'Id: {self.id}, name: {self.name}'

	class Meta:
		verbose_name = "Shop"
		verbose_name_plural = "Shops"


class ShopFeedback(models.Model):
	comment = models.TextField()
	raiting = models.PositiveIntegerField(choices=VERBOSE_RAITING_TYPE, default=1)
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="feedbacks")

	def __str__(self):
		return f"{self.shop}|{self.raiting}"

	class Meta:
		verbose_name = "Shop Feedback"
		verbose_name_plural = "Shop Feedbacks"


class ShopMember(models.Model):
	user = models.OneToOneField(TelegramUser, on_delete = models.CASCADE, related_name="member")
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="members")

	def __str__(self):
		return f"{self.shop}|{self.user}"

	class Meta:
		verbose_name = "Shop employee"
		verbose_name_plural = "Shop employees"


class OrderCredential(models.Model):
	address = models.CharField(max_length=400, blank=True, null=True)
	courier = models.ForeignKey(Courier, on_delete = models.CASCADE, related_name="credentials", null=True, blank=True)
	is_delivery = models.BooleanField()
	phone = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		s = f'Address: {self.address}, '
		if self.courier is not None:
			s += f'Courier: {self.courier}, '
		if self.is_delivery == True:
			s += f'Delivery, '
		else:
			s += 'Pickup '

		s += f'Phone: {self.phone}'
		return s
	class Meta:
		verbose_name = "Order credential"
		verbose_name_plural = "Order credentials"


class OrderOffer(models.Model):
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="offers")
	price = models.FloatField()
	order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='offers')

	def __str__(self):
		return f"Id: {self.id}, from shop: {self.shop}, price: {self.price}"

	class Meta:
		verbose_name = "Order offer"
		verbose_name_plural = "Order offers"


class Order(models.Model):
	customer = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="orders")
	credential = models.OneToOneField(OrderCredential, on_delete=models.CASCADE, related_name="order", null=True, blank=True, db_index=True)
	model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="orders")
	status = models.PositiveSmallIntegerField(choices=VERBOSE_ORDER_TYPE, default=0)
	additional = models.TextField()
	offer = models.OneToOneField(OrderOffer, on_delete=models.CASCADE, null=True, related_name='+', blank=True)
	datetime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Id:{self.id}, order from: {self.customer}| Order status: {self.status}"

	class Meta:
		verbose_name = "Order"
		verbose_name_plural = "Orders"


class ShopRegistrationCode(models.Model):
	code = models.TextField()
	used = models.BooleanField(default=False)
	user = models.BigIntegerField(null=True)
	creation_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Shop invite code."
		verbose_name_plural = "Shop invite codes."

class ShopMemberRegistrationCode(models.Model):
	code = models.TextField()
	used = models.BooleanField(default=False)
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
	creation_time = models.DateTimeField(auto_now_add=True)

class ShopOrdersBlacklist(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

class CourierOrdersBlacklist(models.Model):
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

class CourierRegistrationCode(models.Model):
	code = models.TextField()
	used = models.BooleanField(default=False)
	user = models.BigIntegerField(null=True)
	creation_time = models.DateTimeField(auto_now_add=True)



class ShopNotification(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
	new_available_orders = models.BigIntegerField(default=0)
	new_active_orders = models.BigIntegerField(default=0)

class UserNotification(models.Model):
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	new_offers = models.BigIntegerField(default=0)
	new_couriers = models.BigIntegerField(default=0)


class MessageToDelete(models.Model):
	tg_id = models.BigIntegerField()
	msg_id = models.BigIntegerField(default=None, null=True)

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



