from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("plant/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.basket, name="basket"),
    path("cart/add/<slug:slug>/", views.add_to_basket, name="add_to_basket"),
    path("cart/update/", views.update_basket, name="update_basket"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/", views.order_success, name="order_success"),
    path("subscribe/", views.subscribe, name="subscribe"),
]
