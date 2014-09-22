from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from scipy import misc
import numpy as np
import time

from .tests import SeleniumTest

class PdiffTest(SeleniumTest):
    fixtures = ['users.json', 'trainingbits.json', 'skills.json', 'topics.json']

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
        # import matplotlib.pyplot as plt
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
    # '''
