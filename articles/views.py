from django.shortcuts import render
from braces import views

# Create your views here.
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from articles.models import Article
from articles.forms import ArticleForm
from cart.forms import CartAddArticleForm
#===========================Article===========================


class ListAArticleView(views.LoginRequiredMixin,
                       views.PermissionRequiredMixin,
                       ListView):
    permission_required = "article.change_article"
    model = Article
    template_name = 'article/lista.html'


class ListArticleView(ListView):
    model = Article
    template_name = 'article/list.html'


class DetailArticleView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailArticleView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = CartAddArticleForm()
        return context


class DeleteArticleView(views.LoginRequiredMixin,
                        views.PermissionRequiredMixin,
                        DeleteView):
    permission_required = "article.change_article"
    model = Article
    success_url = reverse_lazy('article_list')
    template_name = 'article/delete.html'


class CreateArticleView(views.LoginRequiredMixin,
                        views.PermissionRequiredMixin,
                        CreateView):
    permission_required = "article.change_article"
    model = Article
    form_class = ArticleForm
    template_name = 'article/create.html'


class UpdateArticleView(views.LoginRequiredMixin,
                        views.PermissionRequiredMixin,
                        UpdateView):
    permission_required = "article.change_article"
    model = Article
    form_class = ArticleForm
    template_name = 'article/update.html'
