#!/usr/bin/env python
__filename = 'nowis_cours_scrape.py'
__fname = 'nowis_cours_scrape'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, argparse, string, ctypes, os, re
import time
from datetime import datetime
import requests
from googletrans import Translator
from bs4 import BeautifulSoup
from selenium import webdriver # pip install -U selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
    #from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    #from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    #from selenium.webdriver.firefox.options import Options

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
WAIT_TIME = 60 # sec
#WAIT_TIME = 60 * 60 # 1 hr

LST_PG_URLS = [
    "https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=1",
    "https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=2"
]

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
def scrape_target_pg(page_url : str):
    ## Selenium: init webdrive ##
    print(f'\nInitializing Selenium webdrive...')
    
    # Configure Selenium options
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode

    # Create a new Selenium driver
    #driver = webdriver.Firefox(options=options) # eg_051723: firefox taking 30sec+
    driver = webdriver.Chrome(options=options)

    ## Selenium: retreive html_content ##
    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    driver.get(page_url)
    html_content = driver.page_source
    
    # translate html_content from french to english (fr -> en)
    translator = Translator(service_urls=['translate.google.com'])
    html_content_trans = translator.translate(html_content, src='fr', dest='en').text
    
    # print both OG & TRANS versions
    print(f"\n\n _ html_content (OG) _ \n{html_content}")
    print(f"\n\n _ html_content (TRANS) _ \n"+html_content_trans)
    
    print(f'\n\n scraping {page_url} _ DONE _')

def get_time_now():
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]

def exe_pg_scrape_loop(lst_pgs : lst, wait_sec : float):
    for pg_url in lst_pgs:
        go_time_start = get_time_now()
        print(f'pg scrape start: {go_time_start}')
        
        scrape_target_pg(pg_url)
        
        print(f'pg scrape start: {go_time_start}')
        print(f'pg scrape end:   {get_time_now()}')
        
        if wait_sec > 0:
            print(f'wait sec... {wait_sec}')
            time.sleep(wait_sec)

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
def go_main():
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}')
    read_cli_args() # print cli args
    argCnt = len(sys.argv) # get arg cnt
    
    # validate args
    if argCnt > 1:
        print('*** ERROR *** _ invalid args\n ... exiting\n\n')
        exit(1)

    # loop through and scrape each url
    exe_pg_scrape_loop(LST_PG_URLS, WAIT_TIME)
    
    print(f'\n\nRUN_TIME_START: {run_time_start}')
    print(f'RUN_TIME_END:   {get_time_now()}')

def read_cli_args():
    funcname = f'<{__filename}> _ ENTER _ read_cli_args'
    print(f'\n{funcname}...')
    argCnt = len(sys.argv)
    print(' # of args: %i' % argCnt)
    print(' argv lst: %s' % str(sys.argv))
    for idx, val in enumerate(sys.argv):
        print(f' argv[{idx}]: {val}')
    print(f'DONE _  read_cli_args...')
    
if __name__ == "__main__":
    go_main()

#ref: https://www.selenium.dev/selenium/docs/api/py/_modules/selenium/webdriver/common/by.html#By
#ref: https://github.com/SeleniumHQ/selenium/blob/a4995e2c096239b42c373f26498a6c9bb4f2b3e7/py/CHANGES
#ref: https://stackoverflow.com/a/72773269/2298002
"""Set of supported locator strategies."""
#ID = "id"
#XPATH = "xpath"
#LINK_TEXT = "link text"
#PARTIAL_LINK_TEXT = "partial link text"
#NAME = "name"
#TAG_NAME = "tag name"
#CLASS_NAME = "class name"
#CSS_SELECTOR = "css selector"



