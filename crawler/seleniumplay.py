from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from crawler.libs.util import get_path
from crawler.module.zettagrid import VirtualDataCenter
import json

d = VirtualDataCenter()
path = get_path('crawler/data/zettagrid.json')
with open(path,'r') as f:
    data = f.read()
    data = json.loads(data)


d.prices = data



###
d = VirtualDataCenter()
driver=d.run()
d.simulate(driver)
d.save_data()


DRIVER_PATH = get_path('chromedriver')

options = Options()
driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
url = 'https://account.zettagrid.id/catalog/product/configure/236/2'
driver.get(url)
act = ActionChains(driver)


form = driver.find_element_by_css_selector('form#orderConfig')
form = driver.find_element_by_css_selector('form#orderConfig')
main_body = form.find_element_by_css_selector('div#container_panel_compute_zone')
main_body.text
compute = main_body.find_elements_by_css_selector('div.panel.panel-info')
compute_details = compute[1].find_element_by_css_selector('div.panel-body')
compute_details = compute_details.find_elements_by_css_selector('div.form-group.row')
processor = compute_details[0].find_elements_by_css_selector('div.input-group')
processor = processor[0]
btn = processor.find_elements_by_css_selector('div#option_821_zg-cdc-processor_spinBtnContainer')
btn = btn[0]
btn_up = btn.find_element_by_css_selector('div#option_821_zg-cdc-processor_upBtn')
btn_up.text
act.move_to_element(btn_up)
act.context_click(btn_up)