from rest_framework.response import Response
from .serializers import OrderSerializer
from rest_framework.generics import (
    DestroyAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView

from .models import Order
from .permissions import IsSessionActive
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from api.menu.models import Menu
from api.order_item.models import OrderItem
from api.coupon.models import Coupon
from django.http import Http404

# Create your views here.


class AddToCart(APIView):

    permission_classes = [IsSessionActive]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get("item_id", None)
        if item_id is None:
            return Response({"message": "Invalid Request"}, status=HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Menu, id=item_id)

        order_item_qs = OrderItem.objects.filter(
            item=item, customer=request.customer, ordered=False
        )

        if order_item_qs.exists():
            order_item = order_item_qs.first()
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(
                item=item, customer=request.customer, ordered=False
            )
            order_item.save()

        order_qs = Order.objects.filter(customer=request.customer, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if not order.items.filter(item__id=order_item.id).exists():
                order.items.add(order_item)
                return Response({"message": "Item added"}, status=HTTP_200_OK)

        else:

            order = Order.objects.create(
                customer=request.customer, table=request.customer.on_table
            )
            order.items.add(order_item)
            return Response({"message": "Item added"}, status=HTTP_200_OK)


class OrderQuantityUpdateView(APIView):
    permission_classes = [IsSessionActive]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get("item_id", None)
        if item_id is None:
            return Response({"message": "Invalid Request"}, status=HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Menu, id=item_id)
        order_qs = Order.objects.filter(customer=request.customer, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__id=item_id).exists():
                order_item = OrderItem.objects.filter(
                    item=item, customer=request.customer, ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    return Response(
                        {
                            "message": "Item quantity updated",
                            "quantity": order_item.quantity,
                        },
                        status=HTTP_200_OK,
                    )

                else:
                    order.items.remove(order_item)
                    order_item.delete()
                    return Response({"message": "Item Removed"}, status=HTTP_200_OK)
            else:
                return Response(
                    {"message": "This item was not in your order list"},
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "You do not have an active order"},
                status=HTTP_400_BAD_REQUEST,
            )


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsSessionActive,)

    def get_object(self):
        try:
            order = Order.objects.get(customer=self.request.customer, ordered=False)
            return order
        except Order.DoesNotExist:
            raise Http404("You do not have an active order")
            # return Response(
            #     {"message": "You do not have an active order"},
            #     status=HTTP_400_BAD_REQUEST,
            # )


class OrderItemDeleteView(DestroyAPIView):
    permission_classes = (IsSessionActive,)
    queryset = OrderItem.objects.all()


class AddCouponView(APIView):
    permission_classes = [IsSessionActive]

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", None)
        paymentType = request.data.get("paymentType", None)

        if code is None:
            return Response(
                {"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST
            )
        order = Order.objects.get(customer=self.request.customer, ordered=False)
        coupon = get_object_or_404(Coupon, code=code, is_active=True)
        if not coupon.multiple_use:
            coupon.is_active = False
            coupon.save()
        order.coupon = coupon
        order.save()
        return Response({"paymentType": paymentType}, status=HTTP_200_OK)


class RemoveCouponView(APIView):
    permission_classes = [IsSessionActive]

    def delete(self, request, *args, **kwargs):
        paymentType = request.data.get("paymentType", None)

        order = Order.objects.get(customer=self.request.customer, ordered=False)

        # coupon = order.coupon
        coupon = Coupon.objects.get(id=order.coupon.id)
        coupon.is_active = True
        coupon.save()
        order.coupon = None

        order.save()
        return Response({"paymentType": paymentType}, status=HTTP_200_OK)


class ConfirmOrderItemView(APIView):
    permission_classes = [IsSessionActive]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get("item_id", None)

        if item_id is None:
            return Response(
                {"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST
            )

        order_item = OrderItem.objects.filter(
            pk=item_id, customer=request.customer, ordered=False
        )
        order_item.update(ordered=True)
        # order_item.save()
        return Response(status=HTTP_200_OK)


class UpdatePaymentType(APIView):
    permission_classes = [IsSessionActive]

    def post(self, request, *args, **kwargs):
        payment_type = request.data.get("payment_type", None)
        if payment_type is None:
            return Response(
                {"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST
            )

        order = Order.objects.filter(customer=request.customer, ordered=False)
        order.update(payment_type=payment_type)
        return Response(status=HTTP_200_OK)


class CheckOTP(APIView):
    permission_classes = [IsSessionActive]

    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp", None)
        if otp is None:
            return Response({"error": "Invalid OTP"}, status=HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(customer=request.customer, ordered=False)[0]
        print(order.otp)
        if int(otp) == int(order.otp):
            return Response({"message": "OK"}, status=HTTP_200_OK)
        else:
            return Response({"error": "Incorrect OTP"}, status=HTTP_400_BAD_REQUEST)

