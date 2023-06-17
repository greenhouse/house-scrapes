#!/usr/bin/env python
__filename = 'kuna_ystory_demo.py'
__fname = 'kuna_ystory_demo'
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
#from translate import Translator
from bs4 import BeautifulSoup
from selenium import webdriver # pip install -U selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
    #from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    #from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    #from selenium.webdriver.firefox.options import Options
import random
import importlib
HTML_1 = importlib.import_module('02_test_kuna_html_1')

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
WAIT_TIME = 10 # sec
WR_HI = 5
WR_LOW = -5

LST_PG_URLS = [ # GET https://yourstory.com/search?page=1&category=Funding
    # NOTE: '?page=0' returns empty lst of results (no err pg|msg)
    "https://yourstory.com/2023/06/weekly-funding-roundup-june-12-16-vc-investments-rise-lenskart",
    "https://yourstory.com/2023/06/lenskart-raises-100-million-chryscapital-private-equity",
    "https://yourstory.com/2023/06/bengaluru-based-home-interior-startup-homelane",
    "https://yourstory.com/2023/06/digital-health-startup-mykare-health-raises-seed-round"
]

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
def scrape_target_pg(driver, page_url : str):
    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
    print('\nGetting page_url content...')
    driver.get(page_url)
    html_content = driver.page_source
    #html_content = HTML_1.TEST_HTML # from 02_test_kuna_html_1.py

    # parse out article descr & body text
    print('\nParsing "description" & "body"...')
    idx_start = html_content.index('"description":"')+len('"description":"')
    idx_end = html_content[idx_start:].index('"')
    descr = html_content[idx_start:idx_start+idx_end+1]
    print('\nDESCR:\n '+descr)
    
    idx_start = html_content.index('"articleBody":"')+len('"articleBody":"')
    idx_end = html_content[idx_start:].index('"')
    body = html_content[idx_start:idx_start+idx_end+1]
    print('\nBODY:\n '+body)

    # print OG html version
    #print(f"\n\n _ html_content (OG) _ \n{html_content}")
    
    # translate html_content from french to english (fr -> en)
    #translator = Translator(service_urls=['translate.google.com'])
    #html_content_trans = translator.translate(html_content, src='fr', dest='en').text

    # print TRANS html version
    #print(f"\n\n _ html_content (TRANS) _ \n"+html_content_trans)

    #print(f'\n\n scraping {page_url} _ DONE _')

def init_webdriver():
    ## Selenium: init webdrive ##
    print(f'\nInitializing Selenium webdriver...')

    # Configure Selenium options
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode

    # Create a new Selenium driver & get html_content
    return webdriver.Chrome(options=options)
    
def exe_pg_scrape_loop(lst_pgs: list, wait_sec : float):
    driver = init_webdriver()
    print(f'# pages to scrape: {len(lst_pgs)}')
    for idx, pg_url in enumerate(lst_pgs):
        go_time_start = get_time_now()
        print(f'\n\npg# {idx+1}\n pg scrape start: {go_time_start}\n    url: {pg_url}')
        scrape_target_pg(driver, pg_url)
        print(f'\n pg scrape start: {go_time_start}\n pg scrape end:   {get_time_now()}\n    url: {pg_url}\n\n')
            
        # if last idx: end
        if idx == len(lst_pgs)-1: print('** NO MORE PAGES **')
        else: # sleep 'wait_sec' before next url
            r_sec = int(random.uniform(wait_sec+WR_LOW, wait_sec+WR_HI))
            wait_sleep(r_sec)
    driver.close()

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
def go_main():
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}')
    lst_argv = read_cli_args() # print cli args

    # validate args
    if len(lst_argv) > 1:
        print('*** ERROR *** _ invalid args\n ... exiting   {get_time_now()}\n\n')
        exit(1)

    # loop through and scrape each url
    exe_pg_scrape_loop(LST_PG_URLS, WAIT_TIME)
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}')

def wait_sleep(wait_sec : int, b_print=True): # sleep 'wait_sec'
    for s in range(wait_sec, 0, -1):
        if b_print: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    print(f'waited... {wait_sec} sec')
        
def get_time_now():
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv

if __name__ == "__main__":
    go_main()



