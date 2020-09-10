from .views import (
    GetDashboardStats,
    GetActiveCustomerView,
    GetOrderDetailView,
    ChangeOrderItemView,
    GetOrderHistoryView,
    MyOrderExportViewSet,
    OrderItemSummary,
    TestHome,
)
from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path("stats/", GetDashboardStats.as_view(), name="get_total_revenue"),
    path("all-orders/", GetActiveCustomerView.as_view(), name="all_active_orders"),
    path("order-detail/<str:pk>", GetOrderDetailView.as_view(), name="order_detail"),
    path(
        "order-item/status/change/", ChangeOrderItemView.as_view(), name="order_detail"
    ),
    path("order-item/", OrderItemSummary.as_view(), name="order_items"),
    path("order-history/", GetOrderHistoryView.as_view(), name="order_history"),
    path(
        "order-history-export/",
        MyOrderExportViewSet.as_view(),
        name="order_history_export",
    ),
    path("home/", TestHome.as_view(), name="home"),
    # path("cash-pay/", payment_cash_card_status, name="payment_cash_card"),
]


urlpatterns += [path("login/", views.obtain_auth_token)]
