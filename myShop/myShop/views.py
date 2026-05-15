from django.shortcuts import render

from store.models import Product, Banner

def home(request):
    products = Product.objects.all().filter(is_available=True)
    banner = Banner.objects.filter(is_active=True).first()

    context = {
        'products': products,
        'banner': banner,
    }

    return render(request, 'index.html', context)