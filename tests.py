from django.test import LiveServerTestCase
from selenium import webdriver
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
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

display_radius = 10

class MySeleniumTests(LiveServerTestCase):
    fixtures = ['users.json', 'trainingbits.json', 'skills.json']

    @classmethod
    def setUpClass(cls):
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
        assert('%s%s' % (self.live_server_url, '/share/') in self.selenium.current_url)


    def test_pdiff(self):
        self.selenium.get('%s' % (self.live_server_url))
        self.selenium.save_screenshot('newscreenshot.png')
        old_image = misc.imread('oldscreenshot.png')
        new_image = misc.imread('newscreenshot.png')
        diff_image = np.copy(new_image)
        for x in range(len(diff_image)):
            for y in range(len(diff_image[x])):
                for u in range(len(diff_image[x][y])):
                    diff_image[x][y][u] = 0
        differences = [[False for y in range(len(new_image[0]))] for x in range(len(new_image))]
        boxes = []
        for x in range(len(new_image)):
            row = new_image[x]
            for y in range(len(row)):
                pixel = row[y]
                different = False
                for u in range(len(pixel)):

                    if new_image[x][y][u] - old_image[x][y][u] != 0:
                        different = True


                differences[x][y] = different

        while any(True in row for row in differences):
            for x in range(len(differences)):
                for y in range(len(differences[0])):
                    if differences[x][y]:
                        array_of_return_values = self.find_borders(x, y, differences, 0, len(differences), 0, len(differences[0]))
                        differences = array_of_return_values.pop()
                        boxes.append(array_of_return_values)

        for box in boxes:
            highest_x = box[0]
            lowest_x = box[1]
            highest_y = box[2]
            lowest_y = box[3]
            for x in range(highest_x - lowest_x):
                current_x = x + lowest_x
                for y in range(highest_y - lowest_y):
                    current_y = y + lowest_y
                    diff_image[current_x][current_y] = new_image[current_x][current_y]


        misc.imsave('pdiff.png', diff_image)

        # Uncomment these lines to have the program stop the testing halfway through and display the image until the window is closed.
        # plt.imshow(diff_image)
        # plt.show()



    def find_borders(self, x, y, array_of_differences, highest_x, lowest_x, highest_y, lowest_y):
        stack = []
        stack.append([x,y])
        array_of_differences[x][y] = False
        while (len(stack) != 0):
            point = stack.pop()
            point_x = point[0]
            point_y = point[1]

            if point_x < lowest_x:
                lowest_x = point_x
            if point_x > highest_x:
                highest_x = point_x
            if point_y < lowest_y:
                lowest_y = point_y
            if point_y > highest_y:
                highest_y = point_y


            for x_radius in range(2*display_radius):
                current_x = point_x + x_radius - display_radius
                if 0 < current_x < len(array_of_differences):
                    for y_radius in range(2*display_radius):
                        current_y = point_y + y_radius - display_radius
                        if 0 < current_y < len(array_of_differences[0]):
                            if array_of_differences[current_x][current_y]:
                                array_of_differences[current_x][current_y] = False
                                stack.append([current_x, current_y])


        return [highest_x, lowest_x, highest_y, lowest_y, array_of_differences]


