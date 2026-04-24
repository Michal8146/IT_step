from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home_alt'), # Alternativní cesta podle dokumentace
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    # Nové cesty pro CRUD:
    path('article/create/', views.create_article, name='create_article'),
    path('article/<int:id>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:id>/delete/', views.delete_article, name='delete_article'),
]