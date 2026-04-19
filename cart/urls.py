from django.urls import path
from .views import CartView, AddToCartView

urlpatterns = [
    path('', CartView.as_view()),
    path('add/', AddToCartView.as_view()),
]