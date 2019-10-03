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
from django import forms
from cliente.models import Cliente, Escala
from .forms import FormInicialEscala

# Create your views here.


def index(request):
    contexto = {
        'meuform': FormInicialEscala(),
        'escala' : Escala()
    }
    return render(request, 'criaEscala.html', contexto)

