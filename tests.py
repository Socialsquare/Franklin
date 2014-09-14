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

    def test_complete_training_bit(self):
        """A specific trainingbit can be completed"""
        MySeleniumTests.login(self)
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/punch-an-angry-shark/view'))
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_class_name('share-button').click()

        assert('%s%s' % (self.live_server_url, '/share/') in self.selenium.current_url)

    def test_complete_skill(self):
        """A specific skill can be completed"""
        MySeleniumTests.login(self)
        self.selenium.get('%s%s' % (self.live_server_url, '/skills'))
        self.selenium.find_element_by_name('skill-name').click()
        # buttons = self.selenium.find_elements_by_name('start-button')
        # print(self.selenium.current_url)
        # correct_button = [button for button in buttons if button.is_displayed()]
        # correct_button[0].click()
        time.sleep(1)
        self.selenium.find_element_by_name('start-button').click()
        # self.selenium.find_element_by_class_name('trainingbit-name').click()

        # self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/punch-an-angry-shark/view'))
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/run-away-from-trouble/view'))
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_class_name('share-button').click()

        print(self.selenium.current_url)
        self.selenium.find_element_by_class_name('skill-flag')
        assert('%s%s' % (self.live_server_url, '/share/') in self.selenium.current_url)


        # for pdiff, use http://scipy-lectures.github.io/advanced/image_processing/. create an array of arrays, each of which stores points.
        # For each point that's different, look for other different points within 10 pixels on each side (maybe change later)
        # Every point that's within 10 pixels, add to the array, and look for points within 10 pixels there. After that, move on to the next
        # Point that hasn't already been added, and add it as an entirely new array of points, repeat until all the points are gone




