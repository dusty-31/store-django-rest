from django.urls import path

from . import views

app_name = 'baskets'


urlpatterns = [
    path('', views.BasketAPIView.as_view()),
    path('<int:pk>', views.BasketAPIView.as_view()),
    path('add', views.BasketLineAPIView.as_view()),
    path('update/<int:pk>', views.BasketLineAPIView.as_view()),
]
