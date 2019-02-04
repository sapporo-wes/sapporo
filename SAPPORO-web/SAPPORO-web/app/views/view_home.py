# coding: utf-8
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "app/home_authenticated.html")
        else:
            return render(request, "app/home.html")
