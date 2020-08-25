# class SetCustomer(object):
from api.customer.models import Customer


def set_customer(get_response):
    def middleware(request):
        # request.META['hello'] = 'world'
        # response['world'] = 'hello'
        try:
            token = request.headers["Customer-Token"]
        except KeyError:
            token = None
        try:
            customer = Customer.objects.get(token=token)
            request.customer = customer
        except Customer.DoesNotExist:
            request.customer = None
        response = get_response(request)
        return response

    return middleware

    # print(request.user)
    # return None
