from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home_alt'), # Alternativní cesta podle dokumentace
    path('article/<int:id>/', views.article_detail, name='article_detail'),
]