from django.shortcuts import render
from .models import Member


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def members(request):
    members = Member.objects.all().values()
    return render(request, "members.html", { "members" : members })
