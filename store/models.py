from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("statement", "Большие растения"),
        ("easy", "Лёгкий уход"),
        ("pet", "Безопасно для питомцев"),
        ("rare", "Особенные"),
    ]
    CARE_CHOICES = [("easy", "Простой"), ("medium", "Умеренный"), ("expert", "Внимательный")]

    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Адрес", max_length=140, unique=True)
    category = models.CharField("Категория", max_length=20, choices=CATEGORY_CHOICES, default="easy")
    short_description = models.CharField("Коротко о растении", max_length=180)
    description = models.TextField("Описание")
    image_url = models.URLField("Фото", max_length=500)
    price = models.DecimalField("Цена, сум", max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    old_price = models.DecimalField("Старая цена, сум", max_digits=12, decimal_places=0, blank=True, null=True)
    care = models.CharField("Сложность ухода", max_length=10, choices=CARE_CHOICES, default="easy")
    light = models.CharField("Освещение", max_length=100, default="Рассеянный свет")
    watering = models.CharField("Полив", max_length=100, default="Когда подсохнет верхний слой")
    stock = models.PositiveIntegerField("В наличии", default=10)
    is_featured = models.BooleanField("Показывать на главной", default=False)
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "name"]
        verbose_name = "растение"
        verbose_name_plural = "растения"

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("confirmed", "Подтверждён"),
        ("shipped", "Передан курьеру"),
        ("done", "Выполнен"),
        ("cancelled", "Отменён"),
    ]
    customer_name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=40)
    email = models.EmailField("Электронная почта", blank=True)
    address = models.CharField("Адрес доставки", max_length=240)
    comment = models.TextField("Комментарий к заказу", blank=True)
    status = models.CharField("Статус", max_length=12, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Заказ №{self.pk} · {self.customer_name}"

    @property
    def total(self):
        return sum((item.price * item.quantity for item in self.items.all()), start=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Растение")
    product_name = models.CharField("Название на момент покупки", max_length=120)
    price = models.DecimalField("Цена за штуку", max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказа"

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"


class Subscriber(models.Model):
    email = models.EmailField("Электронная почта", unique=True)
    created_at = models.DateTimeField("Подписан", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "подписчик"
        verbose_name_plural = "подписчики"

    def __str__(self):
        return self.email
