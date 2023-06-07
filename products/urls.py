from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('products', views.ProductAPIView.as_view(), name='product_list'),
    path('products/<int:pk>', views.ProductAPIView.as_view(), name='product_detail'),
    path('categories', views.CategoryAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>', views.CategoryAPIView.as_view(), name='category-detail'),
]
