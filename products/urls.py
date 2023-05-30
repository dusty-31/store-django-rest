from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('products', views.ProductAPIView.as_view()),
    path('product/<int:pk>', views.ProductAPIView.as_view()),
    path('categories', views.CategoryAPIView.as_view()),
    path('category/<int:pk>', views.CategoryAPIView.as_view()),
]
