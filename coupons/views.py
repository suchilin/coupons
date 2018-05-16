from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.views import View
from coupons.models import Coupon
from coupons.forms import CouponForm, CouponApplyForm
from django.utils import timezone
from braces import views
#===========================Coupon===========================


class CouponApplyView(View):
    form_class = CouponApplyForm

    def post(self, request):
        now = timezone.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
        return redirect('cart:cart_detail')


class ListACouponView(views.LoginRequiredMixin,
                      views.PermissionRequiredMixin,
                      ListView):
    permission_required = "coupons.change_coupons"
    model = Coupon
    template_name = 'coupon/lista.html'


class ListCouponView(ListView):
    model = Coupon
    template_name = 'coupon/list.html'


class DetailCouponView(UpdateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'coupon/details.html'


class DeleteCouponView(views.LoginRequiredMixin,
                       views.PermissionRequiredMixin,
                       DeleteView):
    permission_required = "coupons.change_coupons"
    model = Coupon
    success_url = reverse_lazy('coupon:coupon_list')
    template_name = 'coupon/delete.html'


class CreateCouponView(views.LoginRequiredMixin,
                       views.PermissionRequiredMixin,
                       CreateView):
    permission_required = "coupons.change_coupons"
    model = Coupon
    form_class = CouponForm
    template_name = 'coupon/create.html'


class UpdateCouponView(views.LoginRequiredMixin,
                       views.PermissionRequiredMixin,
                       UpdateView):
    permission_required = "coupons.change_coupons"
    model = Coupon
    form_class = CouponForm
    template_name = 'coupon/update.html'
