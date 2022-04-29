from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,DeleteView,UpdateView,ListView

# Create your views here.
def homeView(request):
    return render(request,'gui/HTML/Home.html')