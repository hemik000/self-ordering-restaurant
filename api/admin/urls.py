from .views import GetDashboardStats
from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path("stats/", GetDashboardStats.as_view(), name="get_total_revenue"),
    # path("capture/", payment_status, name="payment_status"),
    # path("cash-pay/", payment_cash_card_status, name="payment_cash_card"),
]


urlpatterns += [path("login/", views.obtain_auth_token)]

