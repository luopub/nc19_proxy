from django.urls import path
from django.views.generic.base import RedirectView
from .views import wish_got_authorize_code

urlpatterns = [
    path('wish/', wish_got_authorize_code),
]
