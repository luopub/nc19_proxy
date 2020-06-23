"""nc19app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# from proxyhome.views import home_view

from django.http import HttpResponse
import os

def read_file_chunks(fn, remove_file = False, buf_size=262144):
    with open(fn, "rb") as f:
        c = f.read(buf_size)
        while c:
            yield c
            c = f.read(buf_size)

    if remove_file:
        os.remove(fn)
    return None


def download_image(request, filename):
    file_path = os.path.join(os.path.split(__file__)[0], filename)
    response = HttpResponse(read_file_chunks(file_path), content_type = 'image/png')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Length'] = os.path.getsize(file_path)
    return response

def root_view(request):
    return download_image(request, 'zucoor-logo-small.png')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('oauth/', include('authaccount.urls')),
    path('proxy/', include('proxies.urls')),
    path('logo.png', root_view),
]
