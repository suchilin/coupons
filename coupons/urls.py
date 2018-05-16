from django.urls import path
from coupons import views


app_name = 'coupons'
urlpatterns = [

    path('', views.ListCouponView.as_view(), name='coupon_list'),
    path('list', views.ListACouponView.as_view(), name='coupon_list_a'),
    path('<int:pk>', views.DetailCouponView.as_view(),
         name='coupon_details'),
    path('add', views.CreateCouponView.as_view(),
         name='coupon_add'),
    path('update/<int:pk>',
         views.UpdateCouponView.as_view(), name='coupon_update'),
    path('delete/<int:pk>',
         views.DeleteCouponView.as_view(), name='coupon_delete'),
    path('apply', views.CouponApplyView.as_view(), name='apply')
]
