from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from scipy import misc
import numpy as np
import time
import string

from .tests import SeleniumTest

display_radius = 10

class PdiffTest(SeleniumTest):
    fixtures = ['users.json', 'trainingbits.json', 'skills.json', 'topics.json']

    def pdiff(self, name, url):
        self.selenium.get('%s' % (url))
        self.selenium.save_screenshot('new_images/%s%s' % (name, '.png'))
        new_image = misc.imread('new_images/%s%s' % (name, '.png'))
        
        try:
            old_image = misc.imread('old_images/%s%s' % (name, '.png'))
        except FileNotFoundError:
            misc.imsave('old_images/%s%s' % (name, '.png'), new_image)
            old_image = misc.imread('old_images/%s%s' % (name, '.png'))

        try:
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

        except IndexError:
            misc.imsave('old_images/%s%s' % (name, '.png'), new_image)
            old_image = misc.imread('old_images/%s%s' % (name, '.png'))

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


        misc.imsave('pdiff/%s%s' % (name, '.png'), diff_image)
        misc.imsave('old_images/%s%s' % (name, '.png'), old_image)
        misc.imsave('new_images/%s%s' % (name, '.png'), new_image)



        # Uncomment these lines to have the program stop the testing halfway through and display the image until the window is closed.
        # import matplotlib.pyplot as plt
        # plt.imshow(diff_image)
        # plt.show()

    def test_pdiff_crawler(self):
        url_list = self.get_urls()
        for url in url_list:
            self.pdiff(self.sanitize_url(url), url)


    def sanitize_url(self, url):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in url if c in valid_chars)

    def get_urls(self):
        stack = []
        stack_record = []
        already_visited = []
        stack.append('%s' % (self.live_server_url))
        while len(stack) != 0:
            current_url = stack.pop()

            self.selenium.get(current_url)
            for link in self.selenium.find_elements_by_tag_name('a'):
                next_url = link.get_attribute('href')
                if  next_url != None and len(next_url) != 0:
                    if next_url not in already_visited:
                        if self.live_server_url in next_url:
                            already_visited.append(next_url)
                            stack.append(next_url)
                            stack_record.append(next_url)

        return stack_record

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
    # '''
