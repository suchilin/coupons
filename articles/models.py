from django.db import models
from django.urls import reverse_lazy

# Create your models here.


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy('article_list')

    def __str__(self):
        return self.name
