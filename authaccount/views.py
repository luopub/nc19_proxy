from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import json
from urllib.parse import urlencode

from proxies.proxy_handler import ProxyHandler
from logutils.logutils import get_logger

logger = get_logger('authaccount')

def wish_got_authorize_code(request):
    """
    As this is the proxy, the code are got from server
    """
    logger.info('wish_got_authorize_code')

    if "REMOTE_ADDR" in request.META:
        logger.debug({str(request.META["REMOTE_ADDR"])})
    if "REMOTE_HOST" in request.META:
        logger.debug({str(request.META["REMOTE_HOST"])})
    if "REMOTE_PORT" in request.META:
        logger.debug({str(request.META["REMOTE_PORT"])})

    for k,v in request.GET.items():
        logger.debug(f'{k} {v}')
    
    # If we got the authorization_code, then redirect and give it to server to get access_token
    url = ProxyHandler.get_server_base_url() + 'oauth/wish/?' + urlencode(request.GET)
    return HttpResponseRedirect(url)
