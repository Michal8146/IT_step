from django.urls import path
from .views import home, about, members

urlpatterns = [
    path('', home, name="home_page"),
    path('about', about, name="about_page"),
    path('members', members, name="members_page"),
]
