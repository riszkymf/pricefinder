from ..libs.util import *
from ..libs.handler import *
from ..libs.app import *
from crawler.settings import *
from datetime import datetime
import json
import requests


def load_crawler_configuration(path):
    files = get_all(path)
    print(files)
    f_yaml = list()
    for f in files:
        try:
            tmp = load_yaml(f)
        except Exception as e:
            print("Error {} ".format(str(e)))
            continue
        finally:
            f_yaml.append(tmp)
    return f_yaml
    


def run(path=CONF_PATH,force_headless=False,force_dump=True,dump_location=DUMP_LOCATION):
    crawler_result = list()
    configs = load_crawler_configuration(path)
    for datas in configs:
        result = list()
        chck = list()
        cfg = datas[0]
        cfg = flatten_dictionaries(cfg['config'])
        cfg['company_name'] = cfg.pop('name')
        product_details = {}
        result_ = {"company": None, "data": list()}
        for row in datas:
            if 'product' not in row:
                continue
            else:
                prods = row['product']
                prods_ = flatten_dictionaries(prods)
                d = ProductCrawler(cfg,**prods_)
                d.is_headless = force_headless
                _company_details = d.company_detail
                d.config_worker()
                dd=d.run()
                d.write_result(d.normalize(dd))
                _tmp = d.crawler_result()
                result_['data'].append(_tmp)
                chck.append(d.normalize(dd))
                d.driver.quit()
                result.append(dd)
        result_['company'] = _company_details
        dump_json_data(result_)
        crawler_result.append(result_)
    return crawler_result

def dump_json_data(data):
    company = data['company']['nm_company']
    filename = "{}.json".format(company.lower())
    path = DUMP_LOCATION + "/" + filename
    generate_file(path,json.dumps(data))



def register_data(data):
    for row in data:
        company_details = row["company"]
        result = register_company(company_details)
        company_name = company_details["nm_company"]
        fail = list()
        for item in row['data']:
            res = register_company_product(company_name,item)
            nm_company_product = None
            try:
                id_company_product = res['message']['id']
            except Exception:
                id_company_product = None
                nm_company_product = item['nm_product_name']
            print(nm_company_product,id_company_product)
            result = register_content(item,id_company_product,nm_company_product)
            fail = fail+result
    return fail