import datetime

from django.db import models
from .constants import VERBOSE_ORDER_TYPE, VERBOSE_RAITING_TYPE
import django.utils.timezone
class Courier(models.Model):
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)

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
	telegram_id = models.IntegerField()
	language = models.CharField(max_length=40)
	courier = models.OneToOneField(Courier, on_delete = models.CASCADE, related_name="telegram_user", null=True, blank=True)

	def __str__(self):
		return f"user:{self.telegram_id}"

	class Meta:
		verbose_name = "Telegram user"
		verbose_name_plural = "Telegram users"


class CarBrand(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Car brand"
		verbose_name_plural = "Car brands"


class CarModel(models.Model):
	brand = models.ForeignKey(CarBrand, on_delete = models.CASCADE, related_name="models")
	name = models.CharField(max_length=30)
	internal_name = models.CharField(max_length=30)
	years = models.CharField(max_length=30)

	def __str__(self):
		return f"{self.brand} {self.name}"

	class Meta:
		verbose_name = "Car model"
		verbose_name_plural = "Car models"

class ShopAvailableModels(models.Model):
	shop_id = models.ForeignKey



class Shop(models.Model):


	name = models.CharField(max_length=30)
	location = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)
	available_models = models.ManyToManyField(CarModel, related_name="shops", )


	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Shop"
		verbose_name_plural = "Shops"


class ShopFeedback(models.Model):
	comment = models.TextField()
	raiting = models.PositiveIntegerField(choices=VERBOSE_RAITING_TYPE, default=0)
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
	address = models.CharField(max_length=30)
	courier = models.ForeignKey(Courier, on_delete = models.CASCADE, related_name="credentials", null=True, blank=True)
	is_delivery = models.BooleanField()
	phone = models.CharField(max_length=30)

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


class Order(models.Model):
	customer = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="orders")
	credential = models.OneToOneField(OrderCredential, on_delete=models.CASCADE, related_name="order", null=True, blank=True)
	model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="orders")
	status = models.PositiveSmallIntegerField(choices=VERBOSE_ORDER_TYPE, default=0)
	product = models.CharField(max_length=100)
	additional = models.TextField()
	datetime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Order from: {self.customer}| Order status: {self.status}"

	class Meta:
		verbose_name = "Order"
		verbose_name_plural = "Orders"


class OrderOffer(models.Model):
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="offers")
	price = models.PositiveIntegerField()
	is_approved = models.BooleanField(default=False)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="offers")

	def __str__(self):
		return f"{self.pk}|{self.shop}"

	class Meta:
		verbose_name = "Order offer"
		verbose_name_plural = "Order offers"


class ShopRegistrationCode(models.Model):
	code = models.TextField()
	used = models.BooleanField(default=False)
	user = models.IntegerField(null=True)
	creation_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Invite codes."
		verbose_name_plural = "Invite codes."