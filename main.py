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

    with open('publicConfig.json') as json_file:
        data = json.load(json_file)
        my_setting_agent = data["settings"]["1"]

    print("Hello World!")

    dir_path = os.path.dirname(os.path.realpath(__file__))

    driver = webdriver.Chrome(executable_path=f"{dir_path}/chromedriver")

    driver.get("http://www.python.org")
    driver.save_screenshot("screenshot.png")

    driver.close()