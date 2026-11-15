from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, NewsletterForm
from .models import Order, OrderItem, Product, Subscriber


def home(request):
    featured = Product.objects.filter(is_featured=True, stock__gt=0)[:4]
    if not featured:
        featured = Product.objects.filter(stock__gt=0)[:4]
    return render(request, "store/home.html", {"featured_products": featured})


def catalog(request):
    products = Product.objects.filter(stock__gt=0)
    category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "popular")
    if category in dict(Product.CATEGORY_CHOICES):
        products = products.filter(category=category)
    if query:
        products = products.filter(name__icontains=query) | products.filter(short_description__icontains=query)
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    else:
        products = products.order_by("-is_featured", "name")
    return render(
        request,
        "store/catalog.html",
        {"products": products, "categories": Product.CATEGORY_CHOICES, "active_category": category, "query": query, "sort": sort},
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category, stock__gt=0).exclude(pk=product.pk)[:3]
    return render(request, "store/product_detail.html", {"product": product, "related_products": related})


def _basket_items(request):
    basket = request.session.get("basket", {})
    products = Product.objects.filter(pk__in=basket.keys())
    items = []
    total = 0
    for product in products:
        quantity = min(max(int(basket.get(str(product.pk), 0)), 0), product.stock)
        if quantity:
            line_total = product.price * quantity
            items.append({"product": product, "quantity": quantity, "line_total": line_total})
            total += line_total
    return items, total


def basket(request):
    items, total = _basket_items(request)
    return render(request, "store/basket.html", {"items": items, "total": total})


@require_POST
def add_to_basket(request, slug):
    product = get_object_or_404(Product, slug=slug)
    basket_data = request.session.get("basket", {})
    current = int(basket_data.get(str(product.pk), 0))
    if product.stock < 1:
        messages.error(request, "Это растение уже закончилось.")
    elif current >= product.stock:
        messages.warning(request, "Больше растений сейчас нет в наличии.")
    else:
        basket_data[str(product.pk)] = current + 1
        request.session["basket"] = basket_data
        messages.success(request, f"{product.name} добавлен в корзину.")
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("basket")


@require_POST
def update_basket(request):
    basket_data = request.session.get("basket", {})
    for key, value in request.POST.items():
        if not key.startswith("quantity_"):
            continue
        product_id = key.removeprefix("quantity_")
        try:
            quantity = max(0, int(value))
        except ValueError:
            return HttpResponseBadRequest("Некорректное количество")
        product = Product.objects.filter(pk=product_id).first()
        if not product or quantity == 0:
            basket_data.pop(str(product_id), None)
        else:
            basket_data[str(product_id)] = min(quantity, product.stock)
    request.session["basket"] = basket_data
    messages.success(request, "Корзина обновлена.")
    return redirect("basket")


def checkout(request):
    items, total = _basket_items(request)
    if not items:
        messages.info(request, "Сначала добавьте растения в корзину.")
        return redirect("catalog")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = Order.objects.create(
                customer_name=form.cleaned_data["name"],
                phone=form.cleaned_data["phone"],
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
                comment=form.cleaned_data["comment"],
            )
            for item in items:
                product = Product.objects.select_for_update().get(pk=item["product"].pk)
                quantity = min(item["quantity"], product.stock)
                if not quantity:
                    continue
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=product.price,
                    quantity=quantity,
                )
                product.stock -= quantity
                product.save(update_fields=["stock"])
            request.session["basket"] = {}
        return redirect("order_success", order_id=order.pk)
    return render(request, "store/checkout.html", {"form": form, "items": items, "total": total})


def order_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id)
    return render(request, "store/order_success.html", {"order": order})


@require_POST
def subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        _, created = Subscriber.objects.get_or_create(email=email)
        if created:
            messages.success(request, "Готово! Будем присылать только хорошие новости о растениях.")
        else:
            messages.info(request, "Этот адрес уже подписан на нашу рассылку.")
    else:
        messages.error(request, "Проверьте адрес электронной почты и попробуйте ещё раз.")
    return redirect("home")
