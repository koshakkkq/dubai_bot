from django.db import models


class Courier(models.Model):
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Курьер"
		verbose_name_plural = "Курьеры"


class CourierFeedback(models.Model):
	comment = models.TextField()
	rating = models.PositiveIntegerField()
	courier = models.ForeignKey(Courier, on_delete = models.CASCADE, related_name="feedbacks")

	def __str__(self):
		return f"{self.courier}|{self.rating}"

	class Meta:
		verbose_name = "Отзыв на курьере"
		verbose_name_plural = "Отзывы на курьере"


class TelegramUser(models.Model):
	telegram_id = models.IntegerField()
	language = models.CharField(max_length=40)
	courier = models.OneToOneField(Courier, on_delete = models.CASCADE, related_name="telegram_user", null=True, blank=True)

	def __str__(self):
		return f"user:{self.telegram_id}"

	class Meta:
		verbose_name = "Пользователь Телеграма"
		verbose_name_plural = "Пользователи Телеграма"


class CarBrand(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Производитель автомобилей"
		verbose_name_plural = "Производители автомобилей"


class CarModel(models.Model):
	brand = models.ForeignKey(CarBrand, on_delete = models.CASCADE, related_name="models")
	name = models.CharField(max_length=30)
	internal_name = models.CharField(max_length=30)
	years = models.CharField(max_length=30)

	def __str__(self):
		return f"{self.brand} {self.name}"

	class Meta:
		verbose_name = "Модель машины"
		verbose_name_plural = "Модели машин"


class Shop(models.Model):
	name = models.CharField(max_length=30)
	location = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)
	available_models = models.ManyToManyField(CarModel, related_name="shops")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Магазин"
		verbose_name_plural = "Магазины"


class ShopFeedback(models.Model):
	comment = models.TextField()
	raiting = models.PositiveIntegerField()
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="feedbacks")

	def __str__(self):
		return f"{self.shop}|{self.raiting}"

	class Meta:
		verbose_name = "Отзыв на магазине"
		verbose_name_plural = "Отзывы на магазин"


class ShopMember(models.Model):
	user = models.OneToOneField(TelegramUser, on_delete = models.CASCADE, related_name="member")
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="members")

	def __str__(self):
		return f"{self.shop}|{self.user}"

	class Meta:
		verbose_name = "Сотрудник магазина"
		verbose_name_plural = "Сотрудники магазина"


class OrderCredential(models.Model):
	adress = models.CharField(max_length=30)
	courier = models.ForeignKey(CourierFeedback, on_delete = models.CASCADE, related_name="credentials", null=True, blank=True)
	is_delivery = models.BooleanField()
	phone = models.CharField(max_length=30)

	def __str__(self):
		return self.adress

	class Meta:
		verbose_name = "Часть заказа"
		verbose_name_plural = "Части заказа"


class Order(models.Model):
	customer = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="orders")
	credential = models.OneToOneField(OrderCredential, on_delete=models.CASCADE, related_name="order", null=True, blank=True)
	model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="orders")
	status = models.CharField(max_length=30)
	product = models.CharField(max_length=100)
	additional = models.TextField()
	datetime =  models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.customer}|{self.status}"

	class Meta:
		verbose_name = "Заказ"
		verbose_name_plural = "Заказы"


class OrderOffer(models.Model):
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name="offers")
	price = models.PositiveIntegerField()
	is_approved = models.BooleanField(default=False)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="offers")

	def __str__(self):
		return f"{self.pk}|{self.shop}"

	class Meta:
		verbose_name = "Заявка на заказ"
		verbose_name_plural = "Заявки на заказ"