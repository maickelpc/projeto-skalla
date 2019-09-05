
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from core import views

urlpatterns = [
    path('', views.hello),
    # url(r'^(?P<pk>[-\w]+)/$', views.PacoteView.as_view(), name='pacote'),
    path('pacotes/<int:pk>/', views.PacoteView.as_view(), name='pacote'),
    path('admin/', admin.site.urls),
]
