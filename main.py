import cv2
import json
import logging
import os
import pathlib
import pytesseract
import requests
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage.metrics import structural_similarity as ssim

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.INFO)
##End Config##


def find_subdirs(path):
    subdirs = [x for x in os.listdir(
        path) if os.path.isdir(os.path.join(path, x))]
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


def take_screenshots(dir_path, sites):
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


def compare_images(img_path_1, img_path_2):
    img1 = cv2.imread(img_path_1)
    img2 = cv2.imread(img_path_2)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    s = ssim(img1, img2)
    return s


def compare_images_in_dirs(dir_path_1, dir_path_2):
    images_pass = True
    for img_path_1 in os.listdir(dir_path_1):
        img_path_1 = os.path.join(dir_path_1, img_path_1)
        img_path_2 = os.path.join(dir_path_2, img_path_1)
        if os.path.isfile(img_path_1) and os.path.isfile(img_path_2):
            s = compare_images(img_path_1, img_path_2)
            if s < 0.9:
                logging.error(f"{img_path_1} and {img_path_2} are different")
                print(f"{img_path_1} and {img_path_2} are different")
                images_pass = False
            else:
                logging.debug(f"{img_path_1} and {img_path_2} are the same")
        else:
            logging.warning(f"{img_path_1} or {img_path_2} does not exist")
    return images_pass


def extract_text_from_image(image_path):
    result = ""
    img = Image.open(image_path)
    result = pytesseract.image_to_string(img)
    result = result.lower()
    result = result.strip()
    return result


def check_images_for_error_words(dir_path, error_words):
    error_word_pass = True
    for img_path in os.listdir(dir_path):
        img_path = os.path.join(dir_path, img_path)
        if os.path.isfile(img_path):
            result = extract_text_from_image(img_path)
            if any(error_word in result for error_word in error_words):
                logging.error(f"{img_path} contains error word")
                print(f"{img_path} contains error word")
                error_word_pass = False
            else:
                logging.debug(f"{img_path} does not contain error word")
        else:
            logging.warning(f"{img_path} does not exist")
    return error_word_pass


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open('config.json') as json_file:
        data = json.load(json_file)
        sites = data["sites"]
        error_words = data["error_words"]

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

    image_status = compare_images_in_dirs(
        most_recent_dir_path, second_most_recent_dir_path)

    error_word_status = check_images_for_error_words(most_recent_dir_path, error_words)

    if http_status & image_status & error_word_status:
        print("All sites passed the status check")
    else:
        print("One or more sites failed the status check")