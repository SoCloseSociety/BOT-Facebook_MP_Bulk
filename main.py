from calendar import c
from itertools import count
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import socket


from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
import pyautogui
import pyperclip
import csv
import pandas as pd
from glob import glob
import os 
import random
import pickle
import re, itertools
from lxml import etree

facebook_email = input("Enter your  facebook email: ")
facebook_password = input("Enter your  facebook password: ")
f = open("message.txt", "r")
massage = f.read()


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")

def is_connected():
  hostname = "one.one.one.one"  
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
     pass # we ignore any errors, returning False
  return False

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()

driver.get("https://www.facebook.com/login")
driver.find_element(By.ID, "email").send_keys(facebook_email)
driver.find_element(By.ID, "pass").send_keys(facebook_password)
driver.find_element(By.ID, "loginbutton").click()
# WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "myDynamicElement"))
cookies = pickle.dump( driver.get_cookies() , open("facebook_cookies.pkl","wb"))
cookies = pickle.load(open("facebook_cookies.pkl", "rb"))

for cookie in cookies:
    driver.add_cookie(cookie)

with open('profile_links.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        if '/' in row[0]:
            print(row[0])

            driver.get(row[0])

            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            div_aria_label = soup.findAll('div', attrs={"aria-label": True})

            for d in div_aria_label:
                if 'Message' == d['aria-label']:
                    print(d)
                    # print("Find")
                    my_xpath = str(xpath_soup(d))
                    WebDriverWait(driver, 60000).until(EC.visibility_of_element_located((By.XPATH, my_xpath)))
                    driver.find_element(By.XPATH, my_xpath).click()

                    WebDriverWait(driver, 60000).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Write to')]")))
                    pyautogui.write(massage)      
                    pyautogui.press('enter')
                    time.sleep(4)
                    print("Done")
                    print("-----------------------------")
                    break



