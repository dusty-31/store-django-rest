from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.CheckoutAPIView.as_view()),
    path('payment_methods', views.PaymentMethodAPIView.as_view()),
]
