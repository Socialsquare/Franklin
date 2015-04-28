import sys, os, time, json, random, string
import os
import time
import json
import random
import string

from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
import requests

from django.utils.text import slugify

sys.path.append('..')
from global_change_lab.settings import BASE_DIR
from global_change_lab.models import User
from skills.models import Project, Like

username = "admin"
password = "123456"


class SeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):

        if os.getenv('FRANKLIN_TEST_FIREFOX'):
            cls.selenium = webdriver.Firefox()
        elif os.getenv('FRANKLIN_TEST_CHROME'):
            # enable browser logging
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = { 'browser':'ALL' }
            cls.selenium = webdriver.Chrome(desired_capabilities=d)
        else:
            cls.selenium = webdriver.PhantomJS()

        super(SeleniumTest, cls).setUpClass()

        # Wait half a second before failing when trying to find an element
        # (see: http://stackoverflow.com/a/19382234/118608)
        cls.selenium.implicitly_wait(0.5)

        # We cannot get anywhere, if we have to respond to an email
        settings.ACCOUNT_EMAIL_VERIFICATION = 'optional'

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTest, cls).tearDownClass()


class SeleniumTestSuite(SeleniumTest):
    fixtures = ['users.json', 'trainingbits.json', 'skills.json', 'topics.json']

    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_css_selector('button[type=submit]').click()

        u = User.objects.get(username=username)
        return u

    def test_front_page_sanity(self):
        self.selenium.get('%s' % (self.live_server_url))
        greet_elem = \
            self.selenium.\
            find_element_by_css_selector("#front-page-greeter .announcement")
        self.assertEqual(greet_elem.text.lower(), "Tell me and I forget.\nTeach me and I remember.\nInvolve me and I learn.\n- Benjamin Franklin".lower())

    def test_login(self):
        self.login()

        expected_url = '%s/welcome' % self.live_server_url

        if settings.ACCOUNT_EMAIL_VERIFICATION == 'mandatory':
            expected_url = '%s/user/confirm-email/' % self.live_server_url

        self.assertIn(expected_url, self.selenium.current_url)

    def test_complete_training_bit(self):
        """A specific trainingbit can be completed"""
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/punch-an-angry-shark/view'))
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_class_name('share-button').click()

        expected_url = '%s/share/' % self.live_server_url
        self.assertIn(expected_url, self.selenium.current_url)

    def test_complete_skill(self):
        """A specific skill can be completed"""
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, '/skills'))
        time.sleep(1)
        self.selenium.find_element_by_name('skill-name').click()
        time.sleep(1)
        self.selenium.find_element_by_name('start-button').click()

        # self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/punch-an-angry-shark/view'))
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/run-away-from-trouble/view'))
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_class_name('share-button').click()

        self.selenium.find_element_by_class_name('skill-flag')
        expected_url = '%s/share/' % self.live_server_url
        self.assertIn(expected_url, self.selenium.current_url)


    # def test_crawler(self):
    #     url_list = self.get_urls()
    #     acceptable_values = [200, 302]
    #     for url in url_list:
    #         self.assertIn(self.get_status_code(url), acceptable_values, 'Broke on: %s' % (url))
    #
    # def get_urls(self):
    #     stack = []
    #     stack_record = []
    #     already_visited = []
    #     stack.append('%s' % (self.live_server_url))
    #     while len(stack) != 0:
    #         current_url = stack.pop()
    #
    #         self.selenium.get(current_url)
    #         for link in self.selenium.find_elements_by_tag_name('a'):
    #             next_url = link.get_attribute('href')
    #             if  next_url != None and len(next_url) != 0:
    #                 if next_url not in already_visited:
    #                     if self.live_server_url in next_url:
    #                         already_visited.append(next_url)
    #                         stack.append(next_url)
    #                         stack_record.append(next_url)
    #
    #     return stack_record

    def get_status_code(self, url):
        try:
            r = requests.head(url)
            return r.status_code
        except requests.ConnectionError:
            return None



    def test_like_skill(self):
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, '/skill/cleaning-nuclear-waste'))
        buttons = self.selenium.find_elements_by_class_name('button')
        for button in buttons:
            if button.text == "LIKE":
                button.click()

        buttons = self.selenium.find_elements_by_class_name('button')
        button_text = [button.text for button in buttons]
        self.assertIn('UNLIKE', button_text)

    def test_like_trainingbit(self):
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/run-away-from-trouble'))
        buttons = self.selenium.find_elements_by_class_name('button')
        for button in buttons:
            if button.text == "LIKE":
                button.click()

        buttons = self.selenium.find_elements_by_class_name('button')
        button_text = [button.text for button in buttons]
        self.assertIn('UNLIKE', button_text)

    def share(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/trainingbit/punch-an-angry-shark/view'))
        share_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        self.selenium.find_element_by_name('name').send_keys(share_name)
        self.selenium.find_element_by_name('content').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_class_name('share-button').click()

        s = Project.objects.get(slug=slugify(share_name))

        return s

    def test_like_share(self):
        user = self.login()
        share = self.share()
        self.selenium.get('%s%s' % (self.live_server_url, '/shares'))
        self.selenium.find_element_by_class_name('project-title').click()
        # Wait a little here?
        self.selenium.find_element_by_css_selector('a[data-gcl-like-button]').click()
 
        # Print `console.log()` entries from the browser
        # for entry in self.selenium.get_log('browser'):
        #     if entry['source'] == 'console-api':
        #         print(entry['message'])

        # new_buttons = self.selenium.find_elements_by_class_name('unlike')
        # self.assertIn(buttons[0], new_buttons)

        self.selenium.find_element_by_css_selector('a[data-gcl-like-button].unlike')

        self.assertIn(share, [l.content_object for l in user.like_set.all()])

    def test_create_skill(self):
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, '/trainer/dashboard'))
        buttons = self.selenium.find_elements_by_class_name('button')
        correctButton = []
        for button in buttons:
            if button.text == "ADD NEW SKILL":
                correctButton = button
        correctButton.click()
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('description').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('topic-pks[]').click()
        dragItems = self.selenium.find_elements_by_class_name('name')
        correctItem = []
        for item in dragItems:
            if item.text == 'Punch an angry shark':
                correctItem = item
        ActionChains(self.selenium).drag_and_drop(correctItem, self.selenium.find_element_by_id('trainingbits-chosen-list')).perform()
        self.selenium.find_element_by_name('name').submit()
        self.assertIn('edit', self.selenium.current_url)

    def test_create_trainingbit(self):
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, '/trainer/dashboard'))
        buttons = self.selenium.find_elements_by_class_name('button')
        correctButton = []
        for button in buttons:
            if button.text == "ADD NEW TRAINING BIT":
                correctButton = button
        correctButton.click()
        self.selenium.find_element_by_name('name').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('description').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('topic-pks[]').click()
        self.selenium.find_element_by_name('name').submit()
        self.assertIn('edit', self.selenium.current_url)


    def test_signup(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/signup/'))
        self.selenium.find_element_by_name('email').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)) + "@mailinator.com")
        self.selenium.find_element_by_name('username').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('password1').send_keys(password)
        self.selenium.find_element_by_name('password2').send_keys(password)
        self.selenium.find_element_by_name('terms').click()
        self.selenium.find_element_by_name('terms').submit()
        self.selenium.find_element_by_class_name('button').click()
        sex_options = self.selenium.find_elements_by_name('sex')
        option_other = [element for element in sex_options if element.get_attribute('value') == 'male'][0]
        option_other.click()
        self.selenium.find_element_by_name('birthdate_0').send_keys('12')
        self.selenium.find_element_by_name('birthdate_1').send_keys('12')
        self.selenium.find_element_by_name('birthdate_2').send_keys('1212')
        select = Select(self.selenium.find_element_by_name('country'))
        # select.deselect_all()
        select.select_by_visible_text('Other')
        select = Select(self.selenium.find_element_by_name('organization'))
        select.select_by_visible_text('No organization')
        self.selenium.find_element_by_name('description').send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        self.selenium.find_element_by_name('description').submit()
        # time.sleep(60)
        self.selenium.find_element_by_name('topic_ids[]').click()
        self.selenium.find_element_by_name('topic_ids[]').submit()
        trainingbit_names = [element.text for element in self.selenium.find_elements_by_class_name('trainingbit-name')]
        self.assertIn("Punch an angry shark", trainingbit_names)
        self.assertIn("Run away from trouble", trainingbit_names)
        skill_names = [element.text for element in self.selenium.find_elements_by_name('skill-name')]
        self.assertIn("RESCUING PANDAS FROM FIRE", skill_names)
        self.assertIn("CLEANING NUCLEAR WASTE", skill_names)
