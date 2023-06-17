#!/usr/bin/env python
__filename = 'test_kuna.py'
__fname = 'test_kuna'
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

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
WAIT_TIME = 30 # sec
#WAIT_TIME = 60 * 60 # 1 hr

LST_PG_URLS = [ # GET https://yourstory.com/search?page=1&category=Funding
    # NOTE: '?page=0' returns empty lst of results (no err pg|msg)
    "https://yourstory.com/2023/06/weekly-funding-roundup-june-12-16-vc-investments-rise-lenskart",
    "https://yourstory.com/2023/06/lenskart-raises-100-million-chryscapital-private-equity"
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

    # print OG html version
    #print(f"\n\n _ html_content (OG) _ \n{html_content}")
    
#    # translate html_content from french to english (fr -> en)
#    translator = Translator(service_urls=['translate.google.com'])
#    html_content_trans = translator.translate(html_content, src='fr', dest='en').text
#
#    # print TRANS html version
#    print(f"\n\n _ html_content (TRANS) _ \n"+html_content_trans)

    print(f'\n\n scraping {page_url} _ DONE _')

def exe_pg_scrape_loop(lst_pgs, wait_sec : float):
    for pg_url in lst_pgs:
        go_time_start = get_time_now()
        print(f'pg scrape start: {go_time_start}')
        scrape_target_pg(pg_url)
        print(f'pg scrape start: {go_time_start}\npg scrape end:   {get_time_now()}')
            
        # sleep 'wait_sec' before next url
        wait_sleep(wait_sec)

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

def wait_sleep(wait_sec, b_print=True): # sleep 'wait_sec'
    for s in range(wait_sec, 0, -1):
        if b_print: print('wait ', s, sep='', end='\n')
        time.sleep(1)
        
def get_time_now():
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv
    
#    funcname = f'<{__filename}> _ ENTER _ read_cli_args'
#    print(f'\n{funcname}...')
#    argCnt = len(sys.argv)
#    print(' # of args: %i' % argCnt)
#    print(' argv lst: %s' % str(sys.argv))
#    for idx, val in enumerate(sys.argv):
#        print(f' argv[{idx}]: {val}')
#    print(f'DONE _  read_cli_args...')

if __name__ == "__main__":
    go_main()



