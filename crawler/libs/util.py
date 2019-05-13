import yaml
import os
import sys
import json
import requests
import random

from os import listdir
from os.path import isfile,isdir,join,abspath
from fake_useragent import UserAgent
from currency_converter import CurrencyConverter

def load_yaml(filename):
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
        f.close()
    return data

def get_path(path):
    cwd = os.getcwd()
    new_path = os.path.join(cwd, path)
    new_path = os.path.abspath(new_path)
    return new_path

def get_all(folder, ignores=list()):
    if not os.path.isabs(folder):
        folder = get_path(folder)
    if ignores:
        for i in ignores:
            if not os.path.isabs(i):
                i = get_path(i)
    files = list()
    dirs = [folder]
    ext = ['yaml','yml']

    def dive(f_data):
        if len(dirs) > 0:
            for d_dir in f_data:
                for d in listdir(d_dir):
                    path = join(d_dir, d)
                    if check_exist(path):
                        if isdir(path) and path not in ignores:
                            dirs.append(path)
                        if isfile(path) and path not in ignores:
                            files.append(path)
                dirs.remove(d_dir)
                break
            return dive(dirs)
    dive(dirs)
    return files
    
def check_exist(path):
    return os.path.exists(path)

def collect_yaml_resource(folder):
    ext = ['yaml', 'yml']
    files_all = [f for f in listdir if isfile(join(folder,f))]
    return files_all


def get_page(url, retries=20):
    while retries > 0:
        user_agent = get_agents()
        headers = {'user-agent': user_agent}
        result = requests.get(url, headers=headers)
        if result.status_code is 200:
            return result
        else:
            retries = retries - 1


def get_rawpage(url, retries=20):
    while retries >= 0:
        result = requests.get(url)
        if result.status_code is 200:
            return result
        else:
            retries = retries - 1

def get_agents():
    dump_file = 'static/fakeagents.json'
    ua = UserAgent(fallback=obtain_useragents())
    return ua.random


def obtain_useragents():
    filepath = 'crawler/static/useragent.yaml'
    user_agents = load_yaml(filepath)
    keys = list(user_agents.keys())
    key = random.choice(keys)
    user_agent = random.choice(user_agents[key])
    return user_agent


def update_useragents():
    ua = UserAgent()
    ua.update()
    from module.useragent import generate_useragents
    generate_useragents()


def lowercase_keys(data):
    result = dict()
    for key, value in data.items():
        result[key.lower()] = value
    return result


def kurs(amount, from_, to_):
    c = CurrencyConverter()
    return c.convert(amount, from_.upper(), to_.upper())

def keypair_to_dict(key_pair):
    d = {}
    for key, val in key_pair:
        d[key] = val
    return d
