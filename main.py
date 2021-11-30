import json
import logging
import os 

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

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open('config.json') as json_file:
        data = json.load(json_file)
        for site in data["sites"]:
            url=site["url"]
            driver.get(url)
            driver.save_screenshot(url.replace("/","_")+".png")

    driver.close()