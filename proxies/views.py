from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from logutils.logutils import get_logger
from .wish_handler import WishHandler

import requests
requests.adapters.DEFAULT_RETRIES = 5

import json


logger = get_logger('authaccount')


def wish_proxy_proc(request, path=''):
    logger.info('wish_proxy_proc: ' + path)
    """
    Proxy receve data in by POST method.
    The data contains at least two fields:
        type: type of request, in string
        data: the data payload.
        if type is wish api call, then data is json in the following format:
            endpoint: endpoint corresponding to wish api definitions
            params: params for GET request
            data: form data for POST request
    """
    # if request.method != 'POST':
        # logger.warning('wish_proxy_proc only accept POST call')
        # return HttpResponse('wish_proxy_proc only accept POST call')

    logger.info('wish_proxy_proc method: ' + request.method)

    r1, r2 = WishHandler.handle(request, path)

    if r1:
        if isinstance(r2, HttpResponse):
            return r2
        else:
            return HttpResponse(json.dumps(r2))
    else:
        return HttpResponseBadRequest('Please check parameter.')

def wish_proxy_proc_api(request, path=''):
    return wish_proxy_proc(request, path = path)

def wish_proxy_serverinfo(request):
    return wish_proxy_proc(request)

def wish_download_file(request):
    """
    Some functions need to download file from wish platform, e.g. product download
    """
    file_path = request.POST.get('file_path', default = '')
    if not file_path:
        return HttpResponseBadRequest('No file path given.')

    res = requests.get(file_path)

    if res.status_code == 200:
        response = HttpResponse(res.iter_content(65536), content_type = res.headers['Content-Type'])
        response['Content-Disposition'] = 'attachment; filename=' + unquote(urlparse(file_path).path.split('/')[-1])
        response['Content-Length'] = res.headers['Content-Length']
        return response

    raise Http404(f'File not found: {file_path}')
