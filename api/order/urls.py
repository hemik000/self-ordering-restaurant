from rest_framework import routers
from django.urls import path, include
from . import views


urlpatterns = [
    path("my/", views.OrderDetailView.as_view(), name="my_order"),
    path("add-to-cart/", views.AddToCart.as_view(), name="add-to-cart"),
    path(
        "update-quantity/",
        views.OrderQuantityUpdateView.as_view(),
        name="update-quantity",
    ),
    path("<str:pk>/delete", views.OrderItemDeleteView.as_view(), name="delete_item"),
    path("coupon/add", views.AddCouponView.as_view(), name="add_coupon"),
    path("coupon/remove", views.RemoveCouponView.as_view(), name="remove_coupon"),
    path("confirm/", views.ConfirmOrderItemView.as_view(), name="confirm_order"),
    path(
        "payment-type/update",
        views.UpdatePaymentType.as_view(),
        name="update_payment_type",
    ),
    path("check-otp/", views.CheckOTP.as_view(), name="check_otp",),
]
