import json
import logging
import os
import pathlib
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.INFO)
##End Config##


def returns_true():
    return True

def find_subdirs(path):
    subdirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    last_2_subdirs = subdirs[-2:]
    return last_2_subdirs

def take_screenshots(dir_path):
    driver = webdriver.Chrome(executable_path=f"{dir_path}/chromedriver")

    new_dir = f"{dir_path}/pictures/{round((time.time()))}"

    pathlib.Path(new_dir).mkdir(parents=True, exist_ok=False)
    
    with open('config.json') as json_file:
        data = json.load(json_file)
        for site in data["sites"]:
            url = site["url"]
            driver.get(url)
            save_path = f"{new_dir}/{url.replace('/', '_')}.png"
            driver.save_screenshot(save_path)
            logging.debug(f"Saved screenshot to {save_path}")
    driver.close()

def get_2_most_recent_dirs(dir_path):
    subdirs = find_subdirs(dir_path)
    last_2_subdirs = subdirs[-2:]
    return last_2_subdirs

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))

    take_screenshots(dir_path)
    
    dirs = find_subdirs(dir_path+"/pictures")
    most_recent_dir = dirs[-1]
    most_recent_dir_path = f"{dir_path}/pictures/{most_recent_dir}"
    second_most_recent_dir = dirs[-2]
    second_most_recent_dir_path = f"{dir_path}/pictures/{second_most_recent_dir}"
    most_recent_pictures = os.listdir(most_recent_dir_path)
    second_most_recent_pictures = os.listdir(second_most_recent_dir_path)    