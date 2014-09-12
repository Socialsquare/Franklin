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

username = "admin"
password = "123456"

def setup_func():
    global driver
    driver = webdriver.Chrome(BASE_DIR + '/chromedriver')


def teardown_func():
    driver.close()

def login():
    driver.get("http://localhost:8000/user/login")
    time.sleep(0.5)
    driver.find_element_by_name('login').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_css_selector('button[type=submit]').click()


@with_setup(setup_func, teardown_func)
def test():
    login()
    driver.get("http://localhost:8000/trainingbit/punch-an-angry-shark/view")
    time.sleep(0.5)
    driver.find_element_by_name('name').send_keys("Punching sharks")
    driver.find_element_by_name('content').send_keys("I punched some sharks")
    driver.find_element_by_class_name('share-button').click()

    time.sleep(0.5)

    assert("http://localhost:8000/share/punching-sharks-" in driver.current_url)

    pass    
