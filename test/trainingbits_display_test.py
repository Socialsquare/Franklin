from selenium import webdriver
# from selenium.wedriver.common.keys import Keys

from nose.tools import eq_, assert_true
from nose import with_setup

import time

import json

import sys

sys.path.append('..')
from global_change_lab.settings import BASE_DIR

driver = None

def setup_func():
    global driver
    driver = webdriver.Chrome(BASE_DIR + '/chromedriver')


def teardown_func():
    driver.close()

@with_setup(setup_func, teardown_func)
def test():
    driver.get("http://localhost:8000/trainingbits")
    time.sleep(0.5)
    trainingbits = driver.find_elements_by_class_name('trainingbit-name')
    print(trainingbits)
    trainingbit_titles = [trainingbit.text for trainingbit in trainingbits]

    print(trainingbit_titles)

    fixture = json.load(open(BASE_DIR + '/skills/fixtures/trainingbits.json'))

    print(fixture)

    all_names = [fixture[i]['fields']['name'] for i in range(len(fixture)) if not fixture[i]['fields']['is_draft']]

    print(all_names)

    for name in all_names:
        if name not in trainingbit_titles:
            assert(False)

    pass    
