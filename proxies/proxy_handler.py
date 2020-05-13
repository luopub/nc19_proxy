import json
from logutils.logutils import get_logger

logger = get_logger('authaccount')

class ProxyHandler():
    server_info = {'scheme': '',  'host': '', 'port': ''}

    # This is the data send here by request
    pdata = {}

    @classmethod
    def parse_data(cls, data):
        '''
            parse input data to dict
        '''
        cls.pdata = data
        
    @classmethod
    def pre_process(cls, request):
        '''
            Do some common work here
            If data is consumed here, return True for first element, 
            second is the status(0 for success) and data
        '''
        cls.parse_data(request.POST)
        
        if cls.pdata['type'] == 'serverinfo':
            cls.server_info['scheme'] = cls.pdata['scheme']
            cls.server_info['host'] = cls.pdata['host']
            cls.server_info['port'] = cls.pdata['port']
            logger.info('serverinfo: {}， {}， {}'.format(cls.server_info['scheme'], cls.server_info['host'], cls.server_info['port']))
            return True, {'status':0, 'data':'OK'}
        return False
        
    @classmethod
    def get_server_base_url(cls):
        return cls.server_info['scheme'] + '://' + cls.server_info['host'] + ':' + cls.server_info['port'] + '/'