from .views import initiate_payment_process, payment_status, payment_cash_card_status
from django.urls import path, include

urlpatterns = [
    path("create/", initiate_payment_process, name="initiate_payment_process"),
    path("capture/", payment_status, name="payment_status"),
    path("cash-pay/", payment_cash_card_status, name="payment_cash_card"),
]

