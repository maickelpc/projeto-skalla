from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required(login_url='/admin/login')
def index(request):
    return render(request, 'index.html',{})


@login_required(login_url='/admin/login')
def minhaEscala(request):
    return render(request, 'minhaescala.html',{})
