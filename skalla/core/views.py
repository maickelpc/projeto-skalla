from django.shortcuts import render
# from django.template import Context, Template
from django.http import HttpResponse
from django.shortcuts import render
from .forms import Formulario
from empresa.models import Empresa
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from django.core.mail import send_mail

# Create your views here.


def hello(request):
    return render(request, 'index.html', {'usuario': 'FULANO'})

