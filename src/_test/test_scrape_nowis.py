#!/usr/bin/env python
__filename = 'pls_burn_scrape.py'
__fname = 'pls_burn_scrape'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

import sys, argparse, string, ctypes, os, re
#import urllib, urllib2, cookielib, httplib
#import cookielib, time, base64
import time
from datetime import datetime

''' requirements
    ref: https://github.com/SeleniumHQ/selenium/blob/trunk/py/docs/source/index.rst
     $ python3 -m pip install -U selenium
'''

#from os import path
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.support.ui import Select
from googletrans import Translator

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
#WAIT_TIME = 60 # sec
WAIT_TIME = 60 * 60 # 1 hr
GO_TIME_START = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
print(f'\n\nGO_TIME_START: {GO_TIME_START}')

i_POST_CNT = -1
#------------------------------------------------------------#
#------------------------------------------------------------#

def go_test_1():
    ## Selenium: init webdrive ##
    run_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    print(f'\nInitializing Selenium webdrive... start: {run_time_start}')
    
    # Configure Selenium options
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode

    # Create a new Selenium driver
    #CLIENT = webdriver.Firefox(options=options) # eg_051723: firefox taking 30sec+
    CLIENT = webdriver.Chrome(options=options)

    ## Selenium: retreive html_content ##
    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    pageUrl = "https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=1"

    #print(f'\n\nConnecting to {pageUrl}... start: {req_time_start}')
    #print(f'... retreiving html_content response')
    CLIENT.get(pageUrl)
    html_content = CLIENT.page_source
    
    # translate html_content from french to english (fr -> en)
    translator = Translator(service_urls=['translate.google.com'])
    html_content_trans = translator.translate(html_content, src='fr', dest='en').text
    
    print(f"\n\n _ html_content (OG) _ \n{html_content}")
    print(f"\n\n _ html_content (TRANS) _ \n"+html_content_trans)
    
    run_time_end = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    print(f'start: {run_time_start}')
    print(f'end:   {run_time_end}')
    
#    print(f'wait... {WAIT_TIME}')
#    time.sleep(WAIT_TIME)
    
    print(f'\n\n scraping {pageUrl} _ DONE _')
    
#def go(i_cnt):
#    loop = i_cnt
#    while loop > 0 or loop < 0:
#        #print(f'\n\n printing plsburn data... loop cnt: {loop}')
#
#        ## Selenium: init webdrive ##
#        cl_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#        print(f'\nInitializing Selenium webdrive... start: {cl_time_start}')
#
#        # Configure Selenium options
#        options = Options()
#        options.add_argument("--headless")  # Run Chrome in headless mode
#
#        # Create a new Selenium driver
#        #CLIENT = webdriver.Firefox(options=options) # eg_051723: firefox taking 30sec+
#        CLIENT = webdriver.Chrome(options=options)
#
#        ## Selenium: retreive html_content ##
#        req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#        pageUrl = "https://plsburn.com/"
#        #print(f'\n\nConnecting to {pageUrl}... start: {req_time_start}')
#        #print(f'... retreiving html_content response')
#        CLIENT.get(pageUrl)
#        html_content = CLIENT.page_source
#
#        resp_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#        #print(f'RECEIVED response -> GET on URL: {pageUrl}... at: {resp_time_start}')
#
#        ## BeautifulSoup: parse html_content ##
#        parse_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#        #print(f'... parsing html_content w/ BeautifulSoup... start: {parse_time_start}\n\n')
#        soup = BeautifulSoup(html_content, "html.parser")
#
#        ## BeautifulSoup: parse html elements sequentially, searching for targets ##
#        div_el = soup.find('div', id='__next')
#        div_elements = div_el.find_all('div')
#        div_elements = div_elements[0].find_all('div', class_='mainSection')
#        div_elements = div_elements[1].find_all('div')
#        div_elements = div_elements[0].find_all('div', class_='barOuter')
#        div_elements = div_elements[0].find_all('div')
#
#        # Loop through target div elements found
#        span_text_perc = 'nil'
#        span_text_proc = 'nil'
#        span_text_dep = 'nil'
#        for div in div_elements:
#            if 'class' in div.attrs:
#                if 'inner' in div['class']:
#                    # Find all child span elements
#                    all_span_els = div.find_all('span')
#                    span_text_perc = all_span_els[0].text # percent
#
#                if 'bottom' in div['class']:
#                    # Find all child span elements
#                    all_span_els = div.find_all('span')
#
#                    span_text_proc = all_span_els[0].text # processed
#                    span_text_dep = all_span_els[1].text # deposited
#
#                    # fix_052123: site removed: 'Processed: ...'
#                    #   removed scraped 'Processed: ...'
#                    #span_text_dep = all_span_els[0].text # deposited
#
#        # fix_052123: site removed: 'Processed: ...'
#        #   manually calculate 'Processed: ...'
#        #f_perc = float(span_text_perc.replace('%', ''))
#        #f_dep = span_text_dep.replace('Deposited:', '')
#        #f_dep = f_dep.replace(',', '')
#        #f_dep = f_dep.replace('$', '')
#        #f_dep = f_dep.replace(' ', '')
#        #f_proc = float(f_dep) * (f_perc * 0.01)
#        #str_f_proc = "{:,.2f}".format(f_proc)
#        #span_text_proc = "Processed: $"+str_f_proc # processed
#
#        print(f'log {pageUrl} scraped text:\n {span_text_perc} complete\n {span_text_dep}\n {span_text_proc}')
#
#        cl_time_end = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#        print(f'start: {cl_time_start}')
#        print(f'end:   {cl_time_end}')
#
#        print(f'wait... {WAIT_TIME}')
#        time.sleep(WAIT_TIME)
#
#        loop = loop if loop < 0 else loop+1
#
#    print(f'\n\n scraping {pageUrl} _ DONE _')
    

def readCliArgs():
    funcname = f'<{__filename}> readCliArgs'
    #print(f'\n{funcname} _ ENTER\n')
    print(f'\nReading CLI args...')
    argCnt = len(sys.argv)
    print(' Number of arguments: %i' % argCnt)
    print(' Argument List: %s' % str(sys.argv))
    for idx, val in enumerate(sys.argv):
        print(' Argv[%i]: %s' % (idx,str(sys.argv[idx])))
    print(f'DONE reading CLI args...')

if __name__ == "__main__":
    readCliArgs()
    argCnt = len(sys.argv)
    i_POST_CNT = -1
    if argCnt > 1:
        i_POST_CNT = int(sys.argv[1])
    else:
        i_POST_CNT = i_POST_CNT
        
#    go(i_POST_CNT)
    go_test_1()
    
    GO_TIME_END = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    print(f'\n\nGO_TIME_START: {GO_TIME_START}')
    print(f'GO_TIME_END:   {GO_TIME_END}')

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



