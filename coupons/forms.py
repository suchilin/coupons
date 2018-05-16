from django import forms
from coupons import models


class CouponForm(forms.ModelForm):

    class Meta:
        model = models.Coupon
        exclude = ('id', )


class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Coupon')
