from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime as dt
from cliente.models import EscalaColaborador, Cliente, PontoAlocacao
from empresa.models import Empresa
from django.utils import timezone
from pytz import timezone as py_timezone
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse

def html2pdf( path: str, params: dict):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)



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

    dInicial = dataInicial + dt.timedelta(hours=0)
    dFinal = dataFinal + dt.timedelta(hours=23)

    c = request.user.id
    escalas = EscalaColaborador.objects.filter(colaborador=c).filter(status__in=[0,1]).filter(dataInicio__gt=dInicial,dataInicio__lt=dFinal).order_by('dataInicio').all()
    colaborador = escalas[0].colaborador

    params = { 'escalas': escalas, 'colaborador': colaborador, 'datainicial': dataInicial, 'datafinal': dataFinal, 'agora': dt.datetime.now()}

    # return html2pdf('imprimirminhaescala.html', params)
    return render(request, 'imprimirminhaescala.html', params)

@login_required(login_url='/admin/login')
def index(request):
    return render(request, 'index.html', {})

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

@login_required(login_url='/admin/login')
def imprimirEscalas(request):
    return render(request, 'imprimirescalas.html',{})


@login_required(login_url='/admin/login')
def imprimirEscala(request):
    timezone.activate('America/Sao_Paulo')
    tz = py_timezone('America/Sao_Paulo')
    dataInicial = request.GET.get('dataInicial', None)
    dataFinal = request.GET.get('dataFinal', None)
    if dataInicial and dataFinal:
        timezone.activate('America/Sao_Paulo')
        dataInicial = tz.localize( dt.datetime.strptime(dataInicial, '%Y-%m-%d') )
        dataFinal = tz.localize( dt.datetime.strptime(dataFinal, '%Y-%m-%d') )
    else:
        dataInicial = dt.datetime.now()
        dataFinal = dataInicial   + dt.timedelta(days=7)

    dInicial = dataInicial + dt.timedelta(hours=0)
    dFinal = dataFinal + dt.timedelta(hours=23)

    tipo = request.GET.get('tipo', None)
    empresa = request.GET.get('empresa', None)
    colaborador = request.GET.get('colaborador', None)
    cliente = request.GET.get('cliente', None)
    ponto = request.GET.get('pontoalocacao', None)

    escalas = EscalaColaborador.objects.filter(dataInicio__gt=dInicial.astimezone(tz),dataInicio__lt=dFinal.astimezone(tz))


    if tipo == 'empresa':
        #pega so os da empersa selecioada
        empresa = int(empresa)
        escalas = escalas = escalas.filter(colaborador__empresa=empresa)
    elif tipo == 'colaborador':
        #pega so os da empersa selecioada
        colaborador = int(colaborador)
        escalas = escalas.filter(colaborador=colaborador)
    elif tipo == 'cliente':
        cliente = int(cliente)
        escalas = escalas.filter(escala__turnoPonto__pontoAlocacao__cliente=cliente)
    elif tipo == 'ponto':
        print(ponto)
        ponto = int(ponto)
        escalas = escalas.filter(escala__turnoPonto__pontoAlocacao=ponto)

    escalas = escalas.filter(status__in=[0,1])
    params = { 'datainicial': dataInicial, 'datafinal': dataFinal, 'agora': dt.datetime.now()}

    datas = []

    dia = dataInicial
    while(dia <= dataFinal):
        print(dia)
        amanha = dia + dt.timedelta(days=1)
        datas.append({ 'data': dia, 'escalas' :escalas.filter(dataInicio__gte=dia, dataInicio__lt=amanha).order_by('dataInicio').all() }  )

        dia = amanha
        print(datas)

    params['datas'] = datas

    if tipo == 'empresa':
        empresa = Empresa.objects.get(pk=empresa)
        params['empresa'] = empresa

        return render(request, 'imprimirescalaempresa.html', params)
    else:
        if(cliente):
            cliente = Cliente.objects.get(pk=cliente)
        else:
            cliente = PontoAlocacao.objects.get(pk=ponto).cliente

        params['cliente'] = cliente

        return render(request, 'imprimirescalacliente.html', params)
