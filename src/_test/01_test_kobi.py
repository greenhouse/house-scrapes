#!/usr/bin/env python
__filename = '01_test_kobi.py'
__fname = '01_test_kobi'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
from _test_support import * # sys, os, re, json
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

# note_062223: error when using HTML_x w/ nath target
#   but can't use --headless anyway (hence, can't use LOCAL_TEST or HTML_x)
#import importlib
#HTML_x = importlib.import_module('06_test_nath_html_1')
HTML_x = None

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
CSV_FILE_PATH = 'TEST_NATH_OUTPUT.csv'

WAIT_TIME = 7 # sec
WR_HI = 0 # wait range
WR_LOW = -4 # wait range

#AUTO_CLICK_WAIT = False
DEBUG_HIDE = True
WRITE_CSV = True
LOCAL_TEST = False
LST_PG_URLS = [ # GET https://www.theknot.com/marketplace  (manual search results in list of vendor links; need API still)
    # search by category & loc: https://www.theknot.com/marketplace/wedding-reception-venues-venice-ca?sort=featured
    "https://www.theknot.com/marketplace/avensole-winery-temecula-ca-960271",
    "https://www.theknot.com/marketplace/etage-venue-reseda-ca-2032873",
    "https://www.theknot.com/marketplace/the-grand-long-beach-long-beach-ca-620906",
    "https://www.theknot.com/marketplace/noor-pasadena-ca-447280"
]
LST_CSV_EXPORT = []

# use 0 wait time for LOCAL_TEST
if LOCAL_TEST: WAIT_TIME = WR_HI = WR_LOW = 0

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
def scrape_target_pg(driver, page_url : str):
    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
    print(  f'\nGetting page_url content... w/ GLOBALS (',
            f'\n DEBUG_HIDE: {DEBUG_HIDE},',
            f'\n WRITE_CSV: {WRITE_CSV},',
            f'\n LOCAL_TEST: {LOCAL_TEST},',
            f'\n WAIT_TIME: {WAIT_TIME+WR_LOW} to {WAIT_TIME+WR_HI} sec',
            f'\n)\n', sep='')
            
    if not LOCAL_TEST:
        # auto-click w/ 'immediate click'
        driver.get(page_url) # GET html page
                
        # gen html obj from webdriver's html src str
        hc = html.fromstring(driver.page_source)
        html_cont_str = driver.page_source
    else:
        hc = html.fromstring(HTML_x.TEST_HTML) # from 05_test_silk_html_1.py
        html_cont_str = HTML_x.TEST_HTML
        driver.quit()
        
    # print OG html version
    #print(f"\n\n _ html_cont (OG) _ \n{html_cont_str}")
    #print('*** break point ***')
    #while True: pass
    
    ## PRINT SCRAPED DATA ##
    #s  = '***'
    #s0 = '\n'+s
    #d  ='#---------------------------------------------------------------------------#'
    #dd ='#===========================================================================#'
    #print(f'\n{d}\n {page_url} \n{d}')                          # page_url (str)
    #print(f'{s} name (text) {s}:\n    {name}')        # name (str)
    #print(f'{s0} city_state (text) {s}:\n    {city_state}')     # city_state (str)
    #print(f'{s0} phone (text) {s}:\n    {phone}')   # phone (str)
    #print(f'{s0} about (text) {s}:\n    {about}')             # about (str)
    
    # RETURN SCRAPED DATA DICT
    return {'page_url':page_url, 'name':name, 'city_state':city_state, 'phone':phone, 'about':about}

def init_webdriver():
    ## Selenium: init webdrive ##
    print(f'\nInitializing Selenium webdriver...')

    # Configure Selenium options
    options = Options()
    #options.add_argument("--headless")  # Run Chrome in headless mode
        # note_062223: receive error (when using --headless)
        #   06_test_nath_html_0_err.py -> 'Access Denied'

    # Create a new Selenium driver & get html_content
    return webdriver.Chrome(options=options)
            
def exe_pg_scrape_loop(lst_pgs: list, wait_sec : float):
    driver = init_webdriver()
    print(f'# pages to scrape: {len(lst_pgs)}')
    for idx, pg_url in enumerate(lst_pgs):
        go_time_start = get_time_now()
        print(f'\n\npg# {idx+1}\n pg scrape start: {go_time_start}\n    url: {pg_url}')
        d = scrape_target_pg(driver, pg_url)
        print(f'\n pg scrape start: {go_time_start}\n pg scrape end:   {get_time_now()}\n    url: {pg_url}\n\n')
        
        # append scraped page data to global list for export
        if d: LST_CSV_EXPORT.append(d)
        
        # validate more pages (sleep between pgs)
        if idx < len(lst_pgs)-1:
            r_sec = int(random.uniform(wait_sec+WR_LOW, wait_sec+WR_HI))
            wait_sleep(r_sec)
        else:
            print('** NO MORE PAGES **')
            
    print(f'** QUITING WEBDRIVER & WRITING DATA TO CSV ({WRITE_CSV}) **')
    driver.quit()
    if WRITE_CSV: write_lst_dict_to_csv(LST_CSV_EXPORT, CSV_FILE_PATH)
    

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
    
if __name__ == "__main__":
    go_main()

