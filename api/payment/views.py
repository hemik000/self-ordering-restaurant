from api.payment.models import Payment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import razorpay
from api.order.models import Order
from rest_framework.permissions import AllowAny
from api.customer.models import Customer
from api.table.models import Table
from api.order.models import Order

# Create your views here.

KEY_ID = "rzp_test_U4xhl2f60ZY1nb"
KEY_SECRET = "wkkx9LsU61tFcpAdlJ6IBBdJ"

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


@api_view(["POST"])
@permission_classes((AllowAny,))
def initiate_payment_process(request):

    try:
        order_id = request.data["order_id"]
        phone_number = request.data["phone_number"]
    except KeyError:
        return Response({"detail": "No order id was provided."})

    try:
        order = Order.objects.get(id=order_id)
        total = order.get_total_after_gst()
    except Order.DoesNotExist:
        return Response({"detail": "Invalid order id"})

    order_amount = int(total * 100)
    order_currency = "INR"
    order_receipt = order_id
    notes = {"phone_number": phone_number}
    print("FLAG 1")
    response = client.order.create(
        dict(
            amount=order_amount,
            currency=order_currency,
            receipt=order_receipt,
            notes=notes,
            payment_capture="0",
        )
    )
    return Response({"data": response})


@api_view(["POST"])
@permission_classes((AllowAny,))
def payment_status(request):

    try:
        payment_detail = {
            "razorpay_payment_id": request.data["razorpay_payment_id"],
            "razorpay_order_id": request.data["razorpay_order_id"],
            "razorpay_signature": request.data["razorpay_signature"],
        }
        amount = request.data["amount"]
        customer = request.customer
        # print(payment_detail, "   ", amount)
    except KeyError:
        return Response({"detail": "Something went wrong"})

    try:
        status = client.utility.verify_payment_signature(payment_detail)
        client.payment.capture(
            payment_detail["razorpay_payment_id"], amount, {"currency": "INR"},
        )
        # customer = Customer.objects.get(id=customer)
        customer.has_paid = True
        customer.is_on_table = False
        customer.token = 0
        table = Table.objects.get(customer=customer.id)
        table.is_occupied = False
        customer.save()
        table.save()
        payment = Payment.objects.create(
            transaction_id=payment_detail["razorpay_payment_id"],
            customer=customer,
            amount=float(amount) / 100,
        )
        order = Order.objects.filter(customer=request.customer, ordered=False)
        order.update(payment=payment, ordered=True)
        return Response({"detail": "ok"})
    except Order.DoesNotExist:
        return Response({"error": "Error in payment"})


@api_view(["POST"])
@permission_classes((AllowAny,))
def payment_cash_card_status(request):

    try:
        amount = request.data["amount"]
        invoice_no = request.data["invoice_no"]
        customer = request.customer
        # print(payment_detail, "   ", amount)
    except KeyError:
        return Response({"detail": "Something went wrong"})

    try:

        # customer = Customer.objects.get(id=customer)
        customer.has_paid = True
        customer.is_on_table = False
        customer.token = 0
        table = Table.objects.get(customer=customer.id)
        table.is_occupied = False
        customer.save()
        table.save()
        payment = Payment.objects.create(
            transaction_id="cash_" + invoice_no, customer=customer, amount=amount,
        )
        order = Order.objects.filter(customer=request.customer, ordered=False)
        order.update(payment=payment, ordered=True)
        return Response({"detail": "ok"})
    except Order.DoesNotExist:
        return Response({"error": "Error in payment"})
