from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from cart.models import Cart, CartItem
from .models import Order, OrderItem
import uuid


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def checkout(request):
    try:
        shipping = 0
        grand_total = 0
        total = 0
        quantity = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity
            quantity += cart_item.quantity

        shipping = (2 * total) / 100
        grand_total = total + shipping

    except:
        cart_items = []
        total = 0
        quantity = 0
        shipping = 0
        grand_total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'orders/checkout.html', context)


@require_http_methods(["POST"])
def place_order(request):
    user = request.user if request.user.is_authenticated else None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items:
            return redirect('cart')

        # Calculate totals
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity

        shipping = (2 * total) / 100
        grand_total = total + shipping

        # Create order
        order = Order.objects.create(
            user=user,
            order_number=str(uuid.uuid4().hex[:20]).upper(),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            address_line_1=request.POST.get('address_line_1'),
            address_line_2=request.POST.get('address_line_2'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            order_total=grand_total,
            order_note=request.POST.get('order_note', ''),
            is_ordered=True,
        )

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                product=cart_item.product,
                order=order,
                quantity=cart_item.quantity,
                product_price=cart_item.product.product_price,
            )

        # Clear cart
        cart_items.delete()

        return redirect('order_placed', order_number=order.order_number)

    except Exception as e:
        return redirect('cart')


def order_placed(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        order_items = OrderItem.objects.filter(order=order)

        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'orders/order_placed.html', context)
    except Order.DoesNotExist:
        return redirect('cart')


def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)
