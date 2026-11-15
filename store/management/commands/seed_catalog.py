from django.core.management.base import BaseCommand

from store.models import Product


PRODUCTS = [
    {
        "name": "Монстера деликатесная", "slug": "monstera-deliciosa", "category": "statement",
        "short_description": "Большие листья и спокойный характер",
        "description": "Монстера — тот самый эффектный сосед, который сразу собирает вокруг себя комнату. Растёт уверенно, любит рассеянный свет и не требует особого внимания. Каждое новое листо появляется с маленьким праздником.",
        "image_url": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=900&q=85",
        "price": 390000, "old_price": 450000, "care": "easy", "light": "Рассеянный свет", "watering": "После подсыхания верхних 3 см", "stock": 8, "is_featured": True,
    },
    {
        "name": "Фикус лирата", "slug": "ficus-lyrata", "category": "statement",
        "short_description": "Скульптурный силуэт для светлой комнаты",
        "description": "Фикус лирата — спокойный акцент с крупными листьями в форме скрипки. Ему понравится светлое место без прямого полуденного солнца и постоянное место в комнате. Поливайте, когда почва сверху подсохнет.",
        "image_url": "https://images.unsplash.com/photo-1597055181300-b5ed6b3fc7a2?auto=format&fit=crop&w=900&q=85",
        "price": 520000, "care": "medium", "light": "Яркий рассеянный свет", "watering": "Когда подсохнут верхние 3–4 см", "stock": 5, "is_featured": True,
    },
    {
        "name": "Замиокулькас", "slug": "zamioculcas", "category": "easy",
        "short_description": "Неприхотливый и всегда собранный",
        "description": "Замиокулькас переживёт небольшие паузы между поливами и отлично чувствует себя даже в глубине комнаты. Это прекрасное первое растение и надёжный друг для насыщенного графика.",
        "image_url": "https://images.unsplash.com/photo-1509423350716-97f2360afbac?auto=format&fit=crop&w=900&q=85",
        "price": 185000, "care": "easy", "light": "От полутени до рассеянного света", "watering": "Редко, после полного подсыхания почвы", "stock": 12, "is_featured": True,
    },
    {
        "name": "Сансевиерия Лауренти", "slug": "sansevieria-laurentii", "category": "easy",
        "short_description": "Графичные листья, минимум забот",
        "description": "Устойчивая сансевиерия легко адаптируется к разному освещению и не обидится, если вы забудете о поливе. Строгие листья добавляют интерьеру красивую вертикаль.",
        "image_url": "https://images.unsplash.com/photo-1593482892290-f54927ae2b0d?auto=format&fit=crop&w=900&q=85",
        "price": 145000, "care": "easy", "light": "Любой, кроме палящего солнца", "watering": "Раз в 2–3 недели, умеренно", "stock": 14, "is_featured": True,
    },
    {
        "name": "Калатея орбифолия", "slug": "calathea-orbifolia", "category": "pet",
        "short_description": "Мягкие полосы и безопасно для хвостов",
        "description": "Крупные округлые листья калатеи украшены серебристыми полосами. Растение не токсично для кошек и собак. Любит влажный воздух и мягкий рассеянный свет — отличный сосед для светлой ванной комнаты.",
        "image_url": "https://images.unsplash.com/photo-1604762524889-3e2fcc145683?auto=format&fit=crop&w=900&q=85",
        "price": 320000, "care": "medium", "light": "Мягкий рассеянный свет", "watering": "Поддерживать почву слегка влажной", "stock": 6, "is_featured": False,
    },
    {
        "name": "Пеперомия Хоуп", "slug": "peperomia-hope", "category": "pet",
        "short_description": "Компактная зелень для полки или стола",
        "description": "Небольшая пеперомия растёт аккуратными округлыми листьями и не занимает много места. Безопасна для домашних питомцев, любит яркий непрямой свет и умеренный полив.",
        "image_url": "https://images.unsplash.com/photo-1525498128493-380d1990a112?auto=format&fit=crop&w=900&q=85",
        "price": 110000, "care": "easy", "light": "Яркий непрямой свет", "watering": "После подсыхания почвы наполовину", "stock": 9, "is_featured": False,
    },
    {
        "name": "Алоказия Полли", "slug": "alocasia-polly", "category": "rare",
        "short_description": "Контрастные листья с характером",
        "description": "Алоказия Полли привлекает внимание тёмными стреловидными листьями с выразительными светлыми прожилками. Ей подойдёт тёплое место без сквозняков, мягкая вода и немного внимания к влажности воздуха.",
        "image_url": "https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=900&q=85",
        "price": 275000, "care": "expert", "light": "Яркий рассеянный свет", "watering": "Регулярно, без застоя воды", "stock": 4, "is_featured": False,
    },
    {
        "name": "Маранта триколор", "slug": "maranta-tricolor", "category": "rare",
        "short_description": "Узорные листья складываются к вечеру",
        "description": "У маранты удивительная привычка: к вечеру её листья поднимаются вверх, словно ладони. Она любит мягкий свет, тёплое место и регулярный, но аккуратный полив.",
        "image_url": "https://images.unsplash.com/photo-1509423350716-97f2360afbac?auto=format&fit=crop&w=900&q=85&sat=-20",
        "price": 245000, "care": "medium", "light": "Полутень или рассеянный свет", "watering": "Поддерживать равномерную влажность", "stock": 7, "is_featured": False,
    },
]


class Command(BaseCommand):
    help = "Добавить стартовый ассортимент VERDE (повторный запуск обновляет товары)."

    def handle(self, *args, **options):
        for product in PRODUCTS:
            slug = product["slug"]
            Product.objects.update_or_create(slug=slug, defaults=product)
        self.stdout.write(self.style.SUCCESS(f"Каталог готов: {len(PRODUCTS)} растений."))
