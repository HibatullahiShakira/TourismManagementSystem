from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
#localhost:8000/store/products
#localhost:8000/store/products/1


@api_view()
def product_list(request):
    return HttpResponse("hi")
