from django.test import LiveServerTestCase
from selenium import webdriver
import time

import os

import json

import random

import string

import sys


sys.path.append('..')
from global_change_lab.settings import BASE_DIR

driver = None

username = "admin"
password = "123456"

class MySeleniumTests(LiveServerTestCase):
    fixtures = ['users.json', 'trainingbits.json', 'skills.json']

    @classmethod
    def setUpClass(cls):
        print(BASE_DIR)
        chromedriver = BASE_DIR + "/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        cls.selenium = webdriver.Chrome(chromedriver)
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_css_selector('button[type=submit]').click()

    def test_front_page_sanity(self):
        self.selenium.get('%s' % (self.live_server_url))
        assert(self.selenium.find_element_by_name("main-headline").text=="CHANGE\nTHE WORLD!")

    def test_login(self):
        MySeleniumTests.login(self)
        assert('%s%s' % (self.live_server_url, '/welcome') in self.selenium.current_url)

    def test_complete_skill(self):
        """A specific skill can be completed"""
        MySeleniumTests.login(self)
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/punch-an-angry-shark/view'))
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_class_name('share-button').click()

        print(self.selenium.current_url)


        assert('%s%s' % (self.live_server_url, '/share/') in self.selenium.current_url)





