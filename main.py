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


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))

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

    driver.close()
