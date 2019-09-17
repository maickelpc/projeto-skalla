
from django.shortcuts import render
import datetime
from datetime import timedelta
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.core.files import temp as tempfile
from django.core.files.uploadedfile import UploadedFile

from .serializers import ColaboradorSerializer
from .models import Colaborador

class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('id','email')

