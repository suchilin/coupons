from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from articles.models import Article
from .cart import Cart
from .forms import CartAddArticleForm
from coupons.forms import CouponApplyForm
from django.contrib.auth.decorators import login_required


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    Product = get_object_or_404(Article, id=product_id)
    form = CartAddArticleForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=Product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    Product = get_object_or_404(Article, id=product_id)
    cart.remove(Product)
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item[
            'update_quantity_form'] = CartAddArticleForm(initial={'quantity': item['quantity'],
                                                                  'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
