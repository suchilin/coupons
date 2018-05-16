from django import forms
from articles import models


class ArticleForm(forms.ModelForm):

    class Meta:
        model = models.Article
        exclude = ('id', 'cart',)
