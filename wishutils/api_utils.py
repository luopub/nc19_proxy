import requests

from requests import ConnectionError
import json
from json.decoder import JSONDecodeError
from urllib.parse import urljoin, urlencode

from logutils.logutils import get_logger

logger = get_logger('api_utils')

requests.adapters.DEFAULT_RETRIES = 5


class JsonRequest:
    @staticmethod
    def json_request(method, url, params=None, data=None, json=None, headers=None):
        logger.debug(f'json_request: method={method}, url={url}, params={params}, data={data}, json={json}, headers={headers}')
        try:
            r = requests.request(method, url, params=params, data=data, json=json, headers=headers)

            if 'Wish-Rate-Limit-Remaining' in r.headers:
                logger.debug('Wish-Rate-Limit-Remaining: ' + r.headers['Wish-Rate-Limit-Remaining'])
            if 'Wish-Request-Id' in r.headers:
                logger.debug('Wish-Request-Id: ' + r.headers['Wish-Request-Id'])

            logger.info(r.headers)

            logger.info(r.text)

            # r = json.loads(r.text)
            return r.text, r.headers
        except ConnectionError as ce:
            logger.error(f'ConnectionError1: {method} {url}: params={str(params)}, data={str(data)}, json={str(json)}, headers={str(headers)}')
            logger.error(f'ConnectionError2: {ce.args}, {ce.errno}, {ce.response}, {ce.filename}, {ce.request}, {ce.strerror}')
        except JSONDecodeError as jde:
            logger.error(f'JSONDecodeError: {method} {url}: params={str(params)}, data={str(data)}, json={str(json)}, headers={str(headers)}, text={r.text}')
        except TypeError as te:
            logger.error(f'TypeError: {method} {url}: params={str(params)}, data={str(data)}, json={str(json)}, text={r.text}')
        return None, None


class WishApiTrans(JsonRequest):
    url_api_base_root = 'https://china-merchant.wish.com/'
    url_api_base_v2 = url_api_base_root + 'api/v2/'
    url_api_base_v3 = url_api_base_root + 'api/v3/'

    endpoint_oauth_authorize = 'v3/oauth/authorize'
    url_oauth_authorize = urljoin(url_api_base_root, endpoint_oauth_authorize)

    endpoint_oauth_access_token = 'oauth/access_token'
    url_access_token = urljoin(url_api_base_v3, endpoint_oauth_access_token)

    endpoints_v2 = [
        "count/infractions",
        "fetch-bd-announcement",
        "fetch-sys-updates-noti",
        "fulfillment/get-confirmed-delivery-countries",
        "fulfillment/get-confirmed-delivery-shipping-carriers-for-country",
        "fulfillment/get-shipping-carriers",
        "get-currency-code",
        "get/infractions",
        "image",
        "noti/fetch-unviewed",
        "noti/get-unviewed-count",
        "noti/mark-as-viewed",
        "product",
        "product/add",
        "product/cancel-download-job",
        "product/change-sku",
        "product/create-download-job",
        "product/disable",
        "product/enable",
        "product/get-all-shipping",
        "product/get-download-job-status",
        "product/get-products-shipping",
        "product/get-shipping",
        "product/get-shipping-setting",
        "product/multi-get",
        "product/remove",
        "product/remove-extra-images",
        "product/update",
        "product/update-multi-shipping",
        "product/update-shipping",
        "returns/create-return-warehouse",
        "returns/disable-return-setting-for-region",
        "returns/edit-return-warehouse",
        "returns/enroll-product-in-returns",
        "returns/get-all-warehouses",
        "returns/get-product-return-settings",
        "returns/get-product-variation-dimensions",
        "returns/set-product-logistics",
        "ticket",
        "ticket/appeal-to-wish-support",
        "ticket/close",
        "ticket/get-action-required",
        "ticket/re-open",
        "ticket/reply",
        "variant",
        "variant/add",
        "variant/bulk-sku-update",
        "variant/cancel-bulk-update-job",
        "variant/change-sku",
        "variant/disable",
        "variant/enable",
        "variant/get-bulk-update-job-failures",
        "variant/get-bulk-update-job-status",
        "variant/get-bulk-update-job-successes",
        "variant/multi-get",
        "variant/update",
        "variant/update-inventory",
        "warehouse/get-all",
    ]
    endpoints_v3 = [
        'brands',
        'currencies',
        'eu_product_compliance/products',
        'eu_product_compliance/products/bulk_update',
        'eu_product_compliance/products/bulk_update/{id}',
        'eu_product_compliance/responsible_person',
        'eu_product_compliance/responsible_person/{id}',
        'fbs/recommendations',
        'fbs/variations/{id}',
        'france_epr_compliance/compliance_status',
        'france_epr_compliance/unique_identification_number',
        'france_epr_compliance/unique_identification_number/{id}',
        'germany_epr_compliance/compliance_status',
        'germany_epr_compliance/epr_registration_number',
        'germany_epr_compliance/epr_registration_number/{id}',
        'merchant/account_details',
        'merchant/currency_settings',
        'merchant/settings',
        'merchant/shipping_settings',
        'merchant/warehouses',
        'merchant/warehouses/{id}',
        'oauth/access_token',
        'oauth/refresh_token',
        'oauth/test',
        'orders',
        'orders/bulk_get',
        'orders/bulk_get/{id}',
        'orders/shipping_carriers',
        'orders/{id}',
        'orders/{id}/address',
        'orders/{id}/refund',
        'orders/{id}/refund_reasons',
        'orders/{id}/tracking',
        'payments/early_payment',
        'payments/invoices/bulk_get',
        'payments/invoices/bulk_get/{id}',
        'penalties',
        'penalties/count',
        'penalties/{id}',
        'product_boost/balance_updates',
        'product_boost/budget',
        'product_boost/campaigns',
        'product_boost/campaigns/{id}',
        'product_boost/campaigns/{id}/metrics',
        'product_boost/campaigns/{id}/product_feedback',
        'product_boost/keywords',
        'products',
        'products/attributes',
        'products/bulk_get',
        'products/bulk_get/{id}',
        'products/bulk_update',
        'products/bulk_update/{id}',
        'products/categories',
        'products/categories/{id}',
        'products/requests',
        'products/requests/{id}',
        'products/variations/colors',
        'products/{id}',
        'products/{id}/calculated_shipping',
        'products/{id}/first_mile_shipping',
        'products/{id}/variations',
        'promotions/campaigns',
        'promotions/campaigns/{id}',
        'promotions/campaigns/{id}/cancel',
        'promotions/eligible_products',
        'promotions/eligible_products/count',
        'ratings/products',
        'tickets',
        'tickets/{id}',
        'tickets/{id}/replies',
        'unification_initiative/countries',
        'webhook/subscriptions',
        'webhook/subscriptions/{id}',
        'webhook/topics',
        'wish_parcel/shipments',
        'wish_parcel/shipments/{id}',
        'wish_parcel/shipping_options',
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
        # if path in cls.endpoints_v3:
        else:
            return cls.url_api_base_v3 + path
        return False
