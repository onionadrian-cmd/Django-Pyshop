from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import condition
from django.utils.decorators import method_decorator

from category.models import Category
from cart.views import _cart_id
from .models import Product, WebsiteCustomization
from cart.models import CartItem
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(category__category_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'keyword': keyword,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


class CustomCSSView(View):
    def get(self, request):
        customization = WebsiteCustomization.get_settings()

        if customization.background_type == 'image' and customization.background_image:
            background_style = f'url({customization.background_image.url})'
        elif customization.background_type == 'gradient':
            background_style = customization.background_gradient
        else:
            background_style = customization.background_color

        css_content = f"""
/* Dynamic Website Customization */
:root {{
    --primary-color: {customization.primary_color};
    --secondary-color: {customization.secondary_color};
    --accent-color: {customization.accent_color};
    --text-color: {customization.text_color};
    --heading-color: {customization.heading_color};
    --button-color: {customization.button_color};
    --button-hover-color: {customization.button_hover_color};
    --link-color: {customization.link_color};
    --link-hover-color: {customization.link_hover_color};
}}

body {{
    color: {customization.text_color};
    background: {background_style};
}}

h1, h2, h3, h4, h5, h6 {{
    color: {customization.heading_color};
}}

a {{
    color: {customization.link_color};
}}

a:hover {{
    color: {customization.link_hover_color};
}}

.btn, button {{
    background-color: {customization.button_color} !important;
    color: {customization.button_text_color} !important;
    border-color: {customization.button_color} !important;
}}

.btn:hover, button:hover {{
    background-color: {customization.button_hover_color} !important;
    color: {customization.button_hover_text_color} !important;
    border-color: {customization.button_hover_color} !important;
}}

.btn-primary {{
    background-color: {customization.primary_color} !important;
    border-color: {customization.primary_color} !important;
}}

.btn-primary:hover {{
    background-color: {customization.button_hover_color} !important;
    border-color: {customization.button_hover_color} !important;
}}

header {{
    background-color: {customization.header_background};
}}

footer {{
    background-color: {customization.footer_background} !important;
    color: {customization.footer_text_color} !important;
}}

footer a {{
    color: {customization.footer_text_color};
}}

.section-pagetop, .bg {{
    background-color: {customization.background_color};
}}

.card {{
    border-color: {customization.primary_color};
}}

.card-header {{
    background-color: {customization.primary_color};
    color: {customization.button_text_color};
}}

.price {{
    color: {customization.secondary_color};
    font-weight: bold;
}}

.icon-lg {{
    color: {customization.primary_color};
}}
"""
        return HttpResponse(css_content, content_type='text/css')
