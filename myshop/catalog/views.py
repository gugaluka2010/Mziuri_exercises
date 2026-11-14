from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.


PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1800},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Mouse", "price": 40},
]


def home(request):
    return HttpResponse('<h1>myshop</h1> Go to /products/')


def about(request):
    return HttpResponse("ეს არის ჩემი ონლაინ მაღაზია")


def product_list(request):
    html = "<h1>Products</h1><ul>"

    for product in PRODUCTS:
        html += f"<li>{product['name']}: {product['price']} ₾</li>"

    html += "</ul>"

    return HttpResponse(html)


def product_detail(request, pk):
    for product in PRODUCTS:
        if product["id"] == pk:
            return HttpResponse(
                f"<h1>{product['name']}</h1>"
                f"<p>Price: {product['price']} ₾</p>"
            )

    raise Http404("Product not found")