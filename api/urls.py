# from django.urls import path, include
# from rest_framework.authtoken import views
from .views import home
from django.urls import path, include

urlpatterns = [
    path("", home, name="api.home"),
    # path("user/", include("api.user.urls")),
    path("customer/", include("api.customer.urls")),
    path("order/", include("api.order.urls")),
    # path("order/item/", include("api.order_item.urls")),
    path("menu/", include("api.menu.urls")),
    path("table/", include("api.table.urls")),
    path("payment/", include("api.payment.urls")),
    path("category/", include("api.category.urls")),
    path("admin/", include("api.admin.urls")),
]

