from django.test import TestCase
from selenium.webdriver.chrome.webdriver import WebDriver
import time

import json

import random

import string

import sys


sys.path.append('..')
from global_change_lab.settings import BASE_DIR

driver = None

username = "admin"
password = "123456"

class skill_complete_test_case(LiveServerTestCase):
    fixtures = ['users.json', 'trainingbits.json', 'skills.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('username')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        self.selenium.find_element_by_css_selector('button[type=submit]').click()


    def test_complete_skill(self):
        """Skill can be completed"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        login()
        driver.get("http://localhost:8000/trainingbit/punch-an-angry-shark/view")
        time.sleep(0.5)
        driver.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        driver.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        driver.find_element_by_class_name('share-button').click()

        time.sleep(0.5)

        print(driver.current_url)

        assert("http://localhost:8000/share/" in driver.current_url)

# from selenium.wedriver.common.keys import Keys




