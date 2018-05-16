from django.urls import path
from articles import views


urlpatterns = [

    path('', views.ListArticleView.as_view(), name='article_list'),
    path('article/', views.ListAArticleView.as_view(), name='article_list'),
    path('article/<int:pk>', views.DetailArticleView.as_view(),
         name='article_details'),
    path('article/add', views.CreateArticleView.as_view(),
         name='article_add'),
    path('article/update/<int:pk>',
         views.UpdateArticleView.as_view(), name='article_update'),
    path('article/delete/<int:pk>',
         views.DeleteArticleView.as_view(), name='article_delete'),
]
