import json
from urllib.parse import urlencode
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from wishutils.api_utils import WishApiTrans, JsonRequest
from logutils.logutils import get_logger
from .proxy_handler import ProxyHandler

logger = get_logger('authaccount')


class WishHandler(ProxyHandler):
    wishapi = None

    @classmethod
    def handle(cls, request, path = ''):
        logger.info('WishHandler handle(): {}, {}, {}'.format(request.method, request.path, request.path_info)) 
        if request.method == 'GET':
            logger.info('WishHandler GET: {}'.format(str(request.GET)))
        if request.method == 'POST':
            # logger.info(f'request fields: {set(dir(request)) - set(dir(object))}')
            # logger.info('WishHandler POST: {}'.format(str(request.POST)))
            # logger.info('WishHandler content_type: {}'.format(str(request.content_type)))
            logger.info('WishHandler body: {}'.format(str(request.body)))
        
        # First check if it is an wish API request
        r1, r2 = cls.handle_wish_apis(request, path)
        if r1:
            return r1, r2
        
        # if not wish api request, data must be POST with 'type' in post data
        if not request.method == 'POST' or not 'type' in request.POST:
            return False, {'status':1001, 'data': 'Data format error'}
            
        # Common request for proxy configuration
        r1, r2 = cls.pre_process(request)
        if r1:
            return r1, r2
            
        logger.warning('Unknown request received')
        return HttpResponseNotFound(path)
            
    @classmethod
    def handle_wish_apis(cls, request, path = ''):
        if not path:
            logger.info('No endpoint for wish api')
            return False, {'status':0, 'data':'OK'}
            
        url = WishApiTrans.get_url_oauth_authorize(path)
        if url:
            return cls.handle_oauth_authorize(request, url)
            
        url = WishApiTrans.get_url_access_token(path)
        if url:
            return cls.handle_get_access_token(request, url)
            
        url = WishApiTrans.get_url_api_v2v3(path)
        if url:
            return cls.handle_url_api_v2v3(request, url)
            
        return False, None
            
    @classmethod
    def handle_oauth_authorize(cls, request, url):
        return True, HttpResponseRedirect(url + '?' + urlencode(request.GET))
            
    @classmethod
    def handle_get_access_token(cls, request, url):
        text, heades = JsonRequest.json_request(request.method, url, params=request.GET)
        if text:
            return True, HttpResponse(text)
        else:
            return True, {'status':1002, 'data':'Get access_token failed'}
            
    @classmethod
    def handle_url_api_v2v3(cls, request, url):
        headers = {}
        if 'HTTP_AUTHORIZATION' in request.META:
            headers['authorization'] = request.META['HTTP_AUTHORIZATION']
        if 'HTTP_LOCALE' in request.META:
            headers['locale'] = request.META['HTTP_LOCALE']
        if getattr(request, 'content_type', None):
            headers['Content-Type'] = getattr(request, 'content_type')

        kwargs = {
            'headers': headers
        }
        if headers.get('Content-Type') == 'application/json':
            kwargs['json'] = json.loads(request.body.decode('utf8'))
        else:
            kwargs['data'] = request.body

        if request.GET:
            kwargs['params'] = request.GET

        text, headers = JsonRequest.json_request(request.method, url, **kwargs)
        if text:
            logger.info('handle_url_api_v2v3 headers: {}'.format(str(headers)))
            response = HttpResponse(text)
            if 'Wish-Rate-Limit-Remaining' in headers:
                response['Wish-Rate-Limit-Remaining'] = headers['Wish-Rate-Limit-Remaining']
            if 'Wish-Request-Id' in headers:
                response['Wish-Request-Id'] = headers['Wish-Request-Id']
            return True, response
        else:
            return True, {'status':1002, 'data':'API call failed: ' + url}
