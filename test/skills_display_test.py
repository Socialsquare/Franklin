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
    driver.get("http://localhost:8000/skills")
    time.sleep(0.5)
    skills = driver.find_elements_by_name('skill-name')
    print(skills)
    skill_titles = [skill.text for skill in skills]

    print(skill_titles)

    fixture = json.load(open(BASE_DIR + '/skills/fixtures/skills.json'))

    print(fixture)

    all_names = [fixture[i]['fields']['name'] for i in range(len(fixture)) if not fixture[i]['fields']['is_draft']]

    print(all_names)

    for name in all_names:
        if name.upper() not in skill_titles:
            assert(False)

    pass    
