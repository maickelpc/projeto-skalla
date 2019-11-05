from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime as dt
from cliente.models import EscalaColaborador
from django.utils import timezone

# Create your views here.
@login_required(login_url='/admin/login')
def index(request):
    return render(request, 'index.html',{})


@login_required(login_url='/admin/login')
def minhaEscala(request):
    return render(request, 'minhaescala.html',{})

@login_required(login_url='/admin/login')
def imprimirMinhaEscala(request):
    timezone.activate('America/Sao_Paulo')
    dataInicial = request.GET.get('dataInicial', None)
    dataFinal = request.GET.get('dataFinal', None)
    if dataInicial and dataFinal:
        dataInicial = dt.datetime.strptime(dataInicial, '%Y-%m-%d')
        dataFinal = dt.datetime.strptime(dataFinal, '%Y-%m-%d')
    else:
        dataInicial = dt.datetime.now()
        dataFinal = dataInicial   + dt.timedelta(days=15)

    dataInicial = dataInicial - dt.timedelta(days=1)
    dataFinal = dataFinal + dt.timedelta(days=1)

    colaborador = request.user.id
    escalas = EscalaColaborador.objects.filter(colaborador=colaborador).filter(dataInicio__gt=dataInicial,dataInicio__lt=dataFinal).all() #.order_by(dataInicial).all()

    return render(request, 'imprimirminhaescala.html', {'escalas': escalas})


@login_required(login_url='/admin/login')
def criaEscala(request):
    return render(request, 'criaescala.html', {})

@login_required(login_url='/admin/login')
def gestaoEscala(request):
    return render(request, 'gestaoescalas.html',{})


@login_required(login_url='/admin/login')
def solicitacoes(request):
    return render(request, 'solicitacoes.html',{})

@login_required(login_url='/admin/login')
def escalas(request):
    return render(request, 'escalas.html',{})
