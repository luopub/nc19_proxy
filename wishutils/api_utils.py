import requests
from requests import ConnectionError
import json
from json.decoder import JSONDecodeError
from urllib.parse import urljoin, urlencode

from logutils.logutils import get_logger

logger = get_logger('api_utils')

class JsonRequest():
    @staticmethod
    def json_request(method, url, params={}, data={}, headers = {}):
        logger.debug(f'json_request: {method}, {url}, {params}, {data}, {headers}')
        try:
            r = requests.request(method, url, params=params, data = data, headers = headers)

            if 'Wish-Rate-Limit-Remaining' in r.headers:
                logger.debug('Wish-Rate-Limit-Remaining: ' + r.headers['Wish-Rate-Limit-Remaining'])
            if 'Wish-Request-Id' in r.headers:
                logger.debug('Wish-Request-Id: ' + r.headers['Wish-Request-Id'])

            logger.info(r.headers)

            logger.info(r.text)

            # r = json.loads(r.text)
            return r.text, r.headers
        except ConnectionError as ce:
            logger.error(f'ConnectionError1: {method} {url}: params={str(params)}, headers={str(headers)}')
            logger.error(f'ConnectionError2: {ce.args}, {ce.errno}, {ce.response}, {ce.winerror}, {ce.filename}, {ce.request}, {ce.strerror}')
        except JSONDecodeError as jde:
            logger.error(f'JSONDecodeError: {method} {url}: params={str(params)}, headers={str(headers)}, text={r.text}')
        except TypeError as te:
            logger.error(f'TypeError: {method} {url}: params={str(params)}, headers={str(headers)}, text={r.text}')
        return None, None

    @staticmethod
    def json_request_get(url, params={}, headers = {}):
        return JsonRequest.json_request('GET', url, params=params, headers=headers)

    @staticmethod
    def json_request_post(url, params={}, data={}, headers = {}):
        return JsonRequest.json_request('POST', url, params=params, data=data, headers=headers)

class WishApiTrans(JsonRequest):
    url_api_base_root = 'https://china-merchant.wish.com/'
    url_api_base_v2 = url_api_base_root + 'api/v2/'
    url_api_base_v3 = url_api_base_root + 'api/v3/'

    endpoint_oauth_authorize = 'v3/oauth/authorize'
    url_oauth_authorize = urljoin(url_api_base_root, endpoint_oauth_authorize)

    endpoint_oauth_access_token = 'oauth/access_token'
    url_access_token = urljoin(url_api_base_v3, endpoint_oauth_access_token)

    endpoints_v2 = [
        'product/add',
        'product',
        'product/update',
        'product/change-sku',
        'product/enable',
        'product/disable',
        'product/remove',
        'product/multi-get',
        'product/remove-extra-images',
        'product/update-shipping',
        'product/update-multi-shipping',
        'product/get-shipping',
        'product/get-all-shipping',
        'product/get-products-shipping',
        'product/get-shipping-setting',
        'product/create-download-job',
        'product/get-download-job-status',
        'product/cancel-download-job',
        'variant/add',
        'variant',
        'variant/update',
        'variant/change-sku',
        'variant/enable',
        'variant/disable',
        'variant/update-inventory',
        'variant/multi-get',
        'variant/bulk-sku-update',
        'variant/get-bulk-update-job-status',
        'variant/get-bulk-update-job-successes',
        'variant/get-bulk-update-job-failures',
        'fulfillment/get-shipping-carriers',
        'fulfillment/get-confirmed-delivery-countries',
        'fulfillment/get-confirmed-delivery-shipping-carriers-for-country',
        'order',
        'order/multi-get',
        'order/multi-get-fbw',
        'order/get-fulfill',
        'order/fulfill-one',
        'order/refund',
        'order/modify-tracking',
        'order/change-shipping',
        'order/create-download-job',
        'order/get-download-job-status',
        'order/cancel-download-job',
        'order/get-confirmed-delivery-countries',
        'order/get-confirmed-delivery-shipping-carriers-for-country',
        'warehouse/get-all',
        'ticket',
        'ticket/get-action-required',
        'fetch-bd-announcement',
        'fetch-sys-updates-noti',
        'noti/fetch-unviewed',
        'noti/mark-as-viewed',
        'noti/get-unviewed-count',
        'count/infractions',
        'get/infractions',
        'ticket/reply',
        'ticket/close',
        'ticket/appeal-to-wish-support',
        'ticket/re-open',
        'product-boost/campaign/get',
        'product-boost/campaign/multi-get',
        'product-boost/campaign/list-low-budget',
        'product-boost/campaign/create',
        'product-boost/campaign/update',
        'product-boost/campaign/update-running',
        'product-boost/campaign/add-budget',
        'product-boost/campaign/stop',
        'product-boost/campaign/cancel',
        'product-boost/campaign/get-performance',
        'product-boost/campaign/get-product-stats',
        'product-boost/campaign/get-product-daily-stats',
        'product-boost/keyword/multi-get',
        'product-boost/keyword/search',
        'product-boost/budget',
        'product-boost/balance/history',
        'product-boost/campaign/validate-bids',
        'fbw/recommended-skus',
        'fbw/inventory-distribution',
        'fbw/shipping-plan/multi-create-and-submit',
        'fbw/shipping-plan/deliver',
        'fbw/shipping-plan/update-logistics-info',
        'fbw/shipping-plan',
        'fbw/shipping-plan/multi-get',
        'fbw/warehouse/get-available',
        'fbw/warehouse',
        'product/fbw-inventory',
        'product/fbw-inventory/multi-get',
        'fbw/shipping-price',
        'fbw/shipping-price/update',
        'product/fbw-sku-history',
        'fbw/fee',
        'fbw/inventory/return',
        'fbw/inventory/return/get',
        'returns/get-all-warehouses',
        'returns/get-product-return-settings',
        'returns/enroll-product-in-returns',
        'returns/get-product-variation-dimensions',
        'returns/set-product-logistics',
        'returns/create-return-warehouse',
        'returns/edit-return-warehouse',
        'returns/disable-return-setting-for-region',
        'image',
        'get-currency-code',
        'get-shipping-carriers',
    ]
    endpoints_v3 = [
        'oauth/access_token',
        'oauth/refresh_token',
        'oauth/test',
        'brands',
        'currencies',
        'epc/enrollments',
        'fbs/recommendations',
        'fbs/variations',
        'penalties/count',
        'penalties',
        'product_boost/campaigns',
        'product_boost/budget',
        'product_boost/campaigns',
        'product_boost/balance_updates',
        'ratings/products',
    ]

    @classmethod
    def get_url_oauth_authorize(cls, path):
        if path[-1] == '/':
            path = path[:-1]
        if cls.endpoint_oauth_authorize == path:
            return cls.url_oauth_authorize
        return False

    @classmethod
    def get_url_access_token(cls, path):
        if path[-1] == '/':
            path = path[:-1]
        if cls.endpoint_oauth_access_token == path:
            return cls.url_access_token
        return False

    @classmethod
    def get_url_api_v2v3(cls, path):
        if path[-1] == '/':
            path = path[:-1]
        if path in cls.endpoints_v2:
            return cls.url_api_base_v2 + path
        if path in cls.endpoints_v3:
            return cls.url_api_base_v3 + path
        return False
