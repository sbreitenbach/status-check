import cv2
import json
import logging
import os
import pathlib
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage.metrics import structural_similarity as ssim

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.DEBUG)
##End Config##

def find_subdirs(path):
    subdirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    last_2_subdirs = subdirs[-2:]
    return last_2_subdirs

def check_response_code(url):
    response = requests.get(url)
    if response.status_code == 200:
        logging.debug(f"{url} is up and running")
        return True
    else:
        logging.error(f"{url} is down with status code {response.status_code}")
        return False

def take_screenshots(dir_path,sites):
    driver = webdriver.Chrome(executable_path=f"{dir_path}/chromedriver")

    new_dir = f"{dir_path}/pictures/{round((time.time()))}"

    pathlib.Path(new_dir).mkdir(parents=True, exist_ok=False)
    
    for site in sites:
        driver.get(site)
        save_path = f"{new_dir}/{site.replace('/', '_')}.png"
        driver.save_screenshot(save_path)
        logging.debug(f"Saved screenshot to {save_path}")
    driver.close()

def get_2_most_recent_dirs(dir_path):
    subdirs = find_subdirs(dir_path)
    last_2_subdirs = subdirs[-2:]
    return last_2_subdirs

def compare_images(img_path_1,img_path_2):
    img1 = cv2.imread(img_path_1)
    img2 = cv2.imread(img_path_2)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    s = ssim(img1, img2)
    return s

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open('config.json') as json_file:
        data = json.load(json_file)
        sites = data["sites"]
    
    http_status = True
    for site in sites:
        if not check_response_code(site):
            http_status = False
    

    take_screenshots(dir_path, sites)
    
    dirs = find_subdirs(dir_path+"/pictures")
    most_recent_dir = dirs[-1]
    most_recent_dir_path = f"{dir_path}/pictures/{most_recent_dir}"
    second_most_recent_dir = dirs[-2]
    second_most_recent_dir_path = f"{dir_path}/pictures/{second_most_recent_dir}"
    most_recent_pictures = os.listdir(most_recent_dir_path)
    second_most_recent_pictures = os.listdir(second_most_recent_dir_path)

    if http_status:
        print("All sites passed the http status check")
    else: 
        print("One or more sites failed the http status check")