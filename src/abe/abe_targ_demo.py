#!/usr/bin/env python
__filename = 'abe_targ_demo.py'
__fname = 'abe_targ_demo'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, argparse, string, ctypes, os, re
import json
import time
from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver # pip install -U selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
    #from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    #from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    #from selenium.webdriver.firefox.options import Options
import random
import importlib
HTML_2 = importlib.import_module('03_test_abe_html_2')

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
WAIT_TIME = 10 # sec
WR_HI = 0
WR_LOW = -5

LOCAL_TEST = False
LST_PG_URLS = [ # GET https://www.target.com/s?searchTerm=airpods+pro
    "https://www.target.com/p/apple-airpods-pro-2nd-generation/-/A-85978612#tabContent-tab-ShippingReturns",
    
#    "https://www.target.com/p/apple-airpods-pro-2nd-generation/-/A-85978612#lnk=sametab",
    "https://www.target.com/p/apple-airpods-max/-/A-82065675?preselect=54191105#lnk=sametab",
    "https://www.target.com/p/airpods-3rd-generation-with-lightning-charging-case/-/A-85978614#lnk=sametab",
    "https://www.target.com/p/apple-airpods-2nd-generation-with-charging-case/-/A-54191097#lnk=sametab"
]

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
def scrape_target_pg(driver, page_url : str):
    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
    print(f'\nGetting page_url content... (LOCAL_TEST: {LOCAL_TEST})\n')
    if not LOCAL_TEST:
        # NOTE_061823: the html retrieved here is differnt than the html rendered in the GUI
        #   this is because the htm source is rendered dynamically on user interaction
        #   hence, can't analyze html source coming from browser,
        #       need to analyze html source coming from here: driver.page_source
        
        # Need to explicitly wait for the presence of an element on the page
        #   note_061823: GUI tab 'Shipping & Returns', needs auto-click
        #    in order to render 'Shipping details' & 'Return details' (for scraping below)
        
        # Randomly receiving error for shipping & returns auto-click requirement
        #   err -> "not clickable at point (402, 580). Other element would receive the click"
        #   note: happens on both immediate click and when using 'WebDriverWait'
        #   note: when using 'WebDriverWait'
        #       same result for both 'presence_of_element_located' & 'element_to_be_clickable'
        driver.get(page_url) # GET html page
        print('attempting to click element w/o waiting...')
        driver.find_element(By.XPATH, "//a[@id='tab-ShippingReturns']").click() # required for 'Shipping & Returns'

        #wait = WebDriverWait(driver, 30)  # Maximum wait time of 30 sec
        #driver.get(page_url) # GET html page
        #print('waiting for element to be located / clickable...')
        ##el = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='tab-ShippingReturns']")))
        #el = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='tab-ShippingReturns']")))
        #el.click()
                
        # gen html obj from webdriver's html src str
        html_cont = html.fromstring(driver.page_source)
        html_cont_str = driver.page_source
    else:
        html_cont = html.fromstring(HTML_2.TEST_HTML) # from 03_test_abe_html_2.py
        html_cont_str = HTML_2.TEST_HTML
        driver.quit()
    
    # print OG html version
    #print(f"\n\n _ html_cont (OG) _ \n{html_cont_str}")
    #print('*** break point ***')
    #while True: pass

    ## retrieve product image asset urls ##
    # <button><div><div><div><picture><img src='...'>
    lst_img_src = html_cont.xpath("//button//div//div//div//picture//img/@src")
        
    ## get 'Highlights' bullet points ##
    # only select the text nodes of <span> elements that have direct text content.
    #   filters empty or whitespace-only text nodes)
    lst_span_text = html_cont.xpath("//ul//div//div//li//span/text()")
    
    ## get 'Specifications' key/values ##
    dict_specs = {}
    lst_h4_tags     = html_cont.xpath("//div//div//div//h4[contains(text(), 'Specifications')]")
    div_par         = lst_h4_tags[0].getparent()
    lst_childs      = div_par.getchildren()
    
    # lst_div_childs[0] = <div> <div><b>key</b>val</div> </div>
    lst_div_childs  = [child for child in lst_childs if child.tag == 'div']
    for idx, child in enumerate(lst_div_childs):
        if child.tag == 'div':
            b_tag = child.getchildren()[0]
            str_val = child.text_content().strip()
            dict_specs[b_tag.text_content()] = str_val

    ## get 'Description' text ##
    str_descr_html = ''
    lst_h4_tags     = html_cont.xpath("//div//div//div//h4[contains(text(), 'Description')]")
    div_par         = lst_h4_tags[0].getparent()
    lst_childs      = div_par.getchildren()
    
    # lst_div_childs[0] = <div> text<br>text<br>... </div>
    lst_div_childs  = [child for child in lst_childs if child.tag == 'div']
    str_descr_html = lst_div_childs[0].text_content()
    
    ## get 'Description' key/values & images ##
    lst_descr_kvs = []
    div_par_par = div_par.getparent()
    lst_div_childs  = [child for child in div_par_par.getchildren() if child.tag == 'div']
    div_tag = lst_div_childs[2]
    lst_div_tags = html_cont.xpath(".//div[@data-test='wellnessBadgeAndDescription']")

    for idx in range(0, len(lst_div_tags), 1):
        div_w_img = lst_div_tags[idx].getchildren()[0]
        div_w_text = lst_div_tags[idx].getchildren()[1]
        
        lst_imgs = div_w_img.xpath(".//picture//img/@src")
        str_img_url = lst_imgs[0]
        str_key = div_w_text.xpath(".//div/text()")[0]
        str_val = div_w_text.text_content().replace(str_key, '').strip()
        lst_descr_kvs.append({str_key:{'img_url':str_img_url, 'descr':str_val}})

    ## get 'Shipping details' & 'Return details' key/vals ##
    dict_ship = {}
    dict_ret = {}
    lst_h4_tags = html_cont.xpath("//div//div//div//div[@class='h-margin-l-default']//h4[text()]")
    for i in range(len(lst_h4_tags)):
        div_par = lst_h4_tags[i].getparent()
        lst_childs      = div_par.getchildren()
        lst_div_childs  = [child for child in lst_childs if child.tag == 'div']
        
        str_key = lst_h4_tags[i].text_content()
        str_val = ''
        for idx, div_child in enumerate(lst_div_childs):
            str_val = str_val + ' ' + div_child.text_content()
            
        if str_key == 'Shipping details':
            dict_ship[str_key] = str_val
        if str_key == 'Return details':
            dict_ret[str_key] = str_val
    
    ## PRINT SCRAPED DATA ##
    s  = '***'
    s0 = '\n'+s
    d  ='#---------------------------------------------------------------------------#'
    dd ='#===========================================================================#'
    print(f'\n{d}\nIMAGES\n{d}')
    print(f'{s} product imgs (list text) {s}:\n{json.dumps(lst_img_src, indent=4)}') # images list
    
    print(f'\n{d}\nDETAILS\n{d}')
    print(f'{s} Highlights (list text) {s}:\n{json.dumps(lst_span_text, indent=4)}') # highlights str
    print(f'{s0} Specifications (key/vals) {s}:\n{json.dumps(dict_specs, indent=4)}') # specs key/vals
    print(f'{s0} Description (text) {s}:\n{str_descr_html}') # descr text
    print(f'{s0} Description (list key/vals) {s}:\n{json.dumps(lst_descr_kvs, indent=4)}') # descr key/vals
    
    print(f'\n{d}\nSHIPPING & RETURNS\n{d}')
    print(f'{s} Shipping details (key/vals) {s}:\n{json.dumps(dict_ship, indent=4)}') # ship details key/vals
    print(f'{s0} Return details (key/vals) {s}:\n{json.dumps(dict_ret, indent=4)}') # return details key/vals

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
        
        # validate more pages (sleep between pgs)
        if idx < len(lst_pgs)-1:
            r_sec = int(random.uniform(wait_sec+WR_LOW, wait_sec+WR_HI))
            wait_sleep(r_sec)
        else:
            print('** NO MORE PAGES **')
    driver.quit()

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



