from decimal import Decimal

from .models import Product


def basket_context(request):
    basket = request.session.get("basket", {})
    products = Product.objects.filter(pk__in=basket.keys(), stock__gt=0)
    count = 0
    total = Decimal("0")
    for product in products:
        quantity = min(max(int(basket.get(str(product.pk), 0)), 0), product.stock)
        count += quantity
        total += product.price * quantity
    return {"basket_count": count, "basket_total": total}
