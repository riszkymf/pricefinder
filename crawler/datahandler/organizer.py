from crawler.libs.util import *


class NormalizedData(object):
    company_name = ''
    product_name = ''
    last_updated = ''
    raw_data = None
    configuraton = None


class NormalizedDomain(NormalizedData):

    domainDataList = list()

    def __init__(self, data, *args, **kwargs):
        self.company_name = data.company_name
        self.product_name = data.product_name
        self.raw_data = list()
        for item in data:
            self.raw_data.append(lowercase_keys(item))

    def normalize_data():
        domainList = list()
        for row in self.raw_data:
            d = {}
            d['domain'] = row.pop('domain', '-')
            if len(row) == 1:
                defaultprice = list(row.values())
                defaultprice = defaultprice[0]
                d['daftar'] = defaultprice
                d['transfer'] = defaultprice
                d['perpanjang'] = defaultprice
            else:
                d['daftar'] = row.pop('daftar', '-')
                d['transfer'] = row.pop('transfer', '-')
                d['perpanjang'] = row.pop('perpanjang', '-')
            domainList.append(d)
        self.domainDataList = domainList


class NormalizedPlesk(NormalizedData):
    
    



class DataTable(object):
    raw_data = None
    table_head = None
    table_data = None

    def __init__(self):
        self.raw_data = dict()
        self.table_data = dict()
        self.table_head = list()

    def append_headers(self, head):
        if head not in self.table_head:
            self.table_data[head] = list()
            self.table_head.append(head)
        
    def add_data(self, head, data):
        self.table_data[head].append(data)
