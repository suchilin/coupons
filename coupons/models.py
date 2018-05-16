from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse_lazy


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def get_absolute_url(self):
        return reverse_lazy('coupon:coupon_list')

    def __str__(self):
        return self.code
