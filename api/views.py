from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    # print(request.customer)
    return JsonResponse({"info": "Server is up and running"})
