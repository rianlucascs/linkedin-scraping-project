


import logging
import unicodedata
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from time import sleep

# url = 'https://www.google.com.br/'

# options = webdriver.ChromeOptions()

# with webdriver.Chrome(options=options) as driver:
#     driver.get(url)

#     print(type(driver))

print(type({"": "a"}))
