from django.core.validators import MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=120, verbose_name="Имя")),
                ("phone", models.CharField(max_length=40, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Электронная почта")),
                ("address", models.CharField(max_length=240, verbose_name="Адрес доставки")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий к заказу")),
                ("status", models.CharField(choices=[("new", "Новый"), ("confirmed", "Подтверждён"), ("shipped", "Передан курьеру"), ("done", "Выполнен"), ("cancelled", "Отменён")], default="new", max_length=12, verbose_name="Статус")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
            ],
            options={"verbose_name": "заказ", "verbose_name_plural": "заказы", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(max_length=140, unique=True, verbose_name="Адрес")),
                ("category", models.CharField(choices=[("statement", "Большие растения"), ("easy", "Лёгкий уход"), ("pet", "Безопасно для питомцев"), ("rare", "Особенные")], default="easy", max_length=20, verbose_name="Категория")),
                ("short_description", models.CharField(max_length=180, verbose_name="Коротко о растении")),
                ("description", models.TextField(verbose_name="Описание")),
                ("image_url", models.URLField(max_length=500, verbose_name="Фото")),
                ("price", models.DecimalField(decimal_places=0, max_digits=12, validators=[MinValueValidator(0)], verbose_name="Цена, сум")),
                ("old_price", models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True, verbose_name="Старая цена, сум")),
                ("care", models.CharField(choices=[("easy", "Простой"), ("medium", "Умеренный"), ("expert", "Внимательный")], default="easy", max_length=10, verbose_name="Сложность ухода")),
                ("light", models.CharField(default="Рассеянный свет", max_length=100, verbose_name="Освещение")),
                ("watering", models.CharField(default="Когда подсохнет верхний слой", max_length=100, verbose_name="Полив")),
                ("stock", models.PositiveIntegerField(default=10, verbose_name="В наличии")),
                ("is_featured", models.BooleanField(default=False, verbose_name="Показывать на главной")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")),
            ],
            options={"verbose_name": "растение", "verbose_name_plural": "растения", "ordering": ["-is_featured", "name"]},
        ),
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="Электронная почта")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Подписан")),
            ],
            options={"verbose_name": "подписчик", "verbose_name_plural": "подписчики", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=120, verbose_name="Название на момент покупки")),
                ("price", models.DecimalField(decimal_places=0, max_digits=12, verbose_name="Цена за штуку")),
                ("quantity", models.PositiveIntegerField(verbose_name="Количество")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order", verbose_name="Заказ")),
                ("product", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="store.product", verbose_name="Растение")),
            ],
            options={"verbose_name": "позиция заказа", "verbose_name_plural": "позиции заказа"},
        ),
    ]
