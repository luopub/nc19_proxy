from django.urls import path
from django.views.generic.base import RedirectView
from .views import wish_proxy_proc, wish_proxy_serverinfo, wish_proxy_proc_api, wish_download_file

urlpatterns = [
    path('wish/downloadfile', wish_download_file),
    path('wish/serverinfo/', wish_proxy_serverinfo),
    path('wish/', wish_proxy_proc),
    path('wish/api/v2/<path:path>', wish_proxy_proc_api),
    path('wish/api/v3/<path:path>', wish_proxy_proc_api),
    path('wish/<path:path>', wish_proxy_proc),
]
