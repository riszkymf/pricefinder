import yaml
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from crawler.libs.util import get_path,flatten_dictionaries
from crawler.module.extractors import *
import json
from time import sleep

"""
Product Crawler class inherit company details from Company Details class.
It will generate crawlers which will be appended to Worker's tasks list"""


DRIVER_PATH = {"chrome": get_path('chromedriver'),
               "firefox": get_path('geckodriver')}


class Worker(object):

    driverType = "chrome"
    driverPath = DRIVER_PATH['chrome']
    driver = None
    task_ = list()

    def __init__(self, *args, **kwargs):
        task_ = list()
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(self.driverPath, options=options)

    def get(self,url):
        self.driver.get(url)
        self.action = ActionChains(self.driver)

class CompanyDetails(object):
    base_url = None
    company_name = None
    product_list = None

    def __init__(self, **kwargs):
        self.base_url = None
        self.company_name = None
        self.product_list = list()
        if kwargs:
            for key, value in kwargs.items():
                try:
                    setattr(self, key, value)
                except:
                    print("Can not set value")
                    pass


class ProductCrawler(CompanyDetails):
    product_name = None
    endpoint = None
    type_ = None
    content = list()
    worker = None
    driver = None
    failure_count = 0
    is_template_path = False
    is_template_content = False
    with_action = False
    chain_query = list()
    display = None

    def __init__(self, config, *args, **kwargs):
        super(ProductCrawler, self).__init__(**config)
        self.content = {}
        self.action_chains = list()
        for key, value in kwargs.items():
            if key == 'name':
                self.product_name = value
            elif key == 'endpoint':
                self.endpoint = value
            elif key == 'type':
                self.type_ = value
            elif key == 'data_display':
                self.display = value
            elif key == 'content':
                for i in value:
                    content_ = self.parse_content(i)
                    self.content = {**self.content, **content_}
            elif key == 'action_chains':
                chain_query = list()
                self.with_action = True
                for i in value:
                    for key, val in i.items():
                        chain_name = key
                        chain = self.parse_action_chains(val)
                        d = {'chain_name': chain_name, 'chain': chain}
                    self.chain_query.append(d)
            else:
                raise ValueError("Wrong Configuration")

    def get_url(self):
        return self.base_url + self.endpoint

    def is_dynamic(self):
        """ Is templating used? """
        return self.is_template_path or self.is_template_content

    def config_worker(self):
        self.worker = Worker()
        worker = self.worker
        url = self.get_url()
        worker.get(url)
        self.driver = worker.driver
        self.driver.maximize_window()
        self.action = worker.action
        self.config_action_chains()
        self.run()

    def config_action_chains(self):
        if self.with_action:
            action_chains = list()
            chain = self.chain_query
            for i in chain:
                tmp = ActionsHandler(self.action, self.driver, 
                                     i['chain'], i['chain_name'])
            action_chains.append(tmp)
            self.action_chains = action_chains

    def obtain_value(self):
        contents = self.content
        for k, v in contents.items():
            for i in v:
                i.extractor.driver = self.driver

    def parse_action_chains(self, actions):
        chains = list()
        for action in actions:
            for act, query in action.items():
                d = {}
                q_ = flatten_dictionaries(query)
                d[act] = q_
                chains.append(d)    
        return chains

    def parse_content(self, content=list()):
        content_handler = list()
        contents = ContentHandler(content)
        return contents.get_value()

#   Obtain data for every action in action chains. 
    def run(self):
        if self.action_chains:
            self.obtain_value()
            for action in self.action_chains:
                for i in range(0, action.repeat):
                    action.run()
                    self.obtain_value()
                    self.write_value()

    def warm_up(self):
        action = self.action_chains[0]
        action.run()

    def write_value(self):
        data = list()
        for key, value in self.content.items():
            val = list()
            for item in value:
                content_ = item.dump_value()
                val.append(content_)
            data.append(val)
            print(content_)
        self.preprocessed_value = data        

class ContentHandler(ProductCrawler):
    content_name = None

    def __init__(self,items):
        for key,val in items.items():
            self.parse_items(val)
            self.content_name = key

    def get_value(self):
        return {self.content_name: self.extractors_}


    def parse_items(self,item):
        extractors_ = list()
        item = flatten_dictionaries(item)
        for key, value in item.items():
            contentValue = flatten_dictionaries(value)
            for key_, val in contentValue.items():
                if key_.lower() == 'extractor':
                    tmp = flatten_dictionaries(val)
                    config = self.build_extractor_configuration(tmp)
                    extractor = Extractors(**config)
                    extractor.value_name = key
                elif key_.lower() == 'postprocess':
                    tmp = flatten_dictionaries(val)
                    extractor.is_postprocessed = True
                    extractor.postprocess.append(tmp)
            extractors_.append(extractor)
        self.extractors_ = extractors_

    def build_extractor_configuration(self, value):
        d = {"type_": None, 
             "value": None, 
             "attribute": None,
             "driver": self.driver}
        for key, val in value.items():
            if key.lower() == 'attribute' or key.lower() == 'attributes':
                d['attribute'] = val
            else:
                d['type_'] = key
                d['value'] = val
        return d


def dict_list_to_list_dict(data):
    if isinstance(data, dict):
        d = list()
        for key, val in data.items():
            for i in val:
                d.append({key: val})
    return d


class DataSorter(object):
    raw_data = None
    display_type = None

    def __init__(self,data,display):
        pass

    def slider_sorter(self,data):
        processedData = list()
        for i in data:
            tmp_data = flatten_dictionaries(i)
            d = {}
            for key, val in tmp_data.items():
                d[key] = val
            processedData.append(d)
        return processedData

    def card_sorter(self, data):
        processedData = list()
        keys = list(data.keys())
        max_index = max([len(val) for val in data.values()])
        for x in range(0, max_index):
            d = {}
            for i in keys:
                try:
                    d[i] = data[i][x]
                except IndexError:
                    d[i] = "None"
            processedData.append(d)
        return processedData
