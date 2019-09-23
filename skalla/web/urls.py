from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.urls import include, path, re_path
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level,
    # and django.contrib.contenttypes.views imports ContentType.
from django.contrib.contenttypes import views as contenttype_views

from .views import opa

class RotasWeb():
    def urls(self):
        urlpatterns = [
            path('/', opa, name='index'),
            # path('login/', self.login, name='login'),
        ]

        return urlpatterns

