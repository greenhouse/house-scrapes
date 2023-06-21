#!/usr/bin/env python
__filename = '06_test_nath.py'
__fname = '06_test_nath'
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
import importlib
HTML_x = importlib.import_module('06_test_nath_html_1')

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
WAIT_TIME = 10 # sec
WR_HI = 0 # wait range
WR_LOW = -5 # wait range

#AUTO_CLICK_WAIT = False
DEBUG_HIDE = True
WRITE_CSV = True
LOCAL_TEST = False
LST_PG_URLS = [ # GET https://www.theknot.com/marketplace  (manual search results in list of vendor links; need API still)
    "https://www.theknot.com/marketplace/the-addison-boca-raton-fl-612010", # search by category & city/state
    "https://www.theknot.com/marketplace/i-thee-wedd-clarksville-tn-2024860" # search by vendor name
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
    
    # TODO: get elements for this page_url (ie. vendor_page)
    #   name, city/state, phone, about, page_url
    
    # print OG html version
    print(f"\n\n _ html_cont (OG) _ \n{html_cont_str}")
    print('*** break point ***')
    while True: pass
    
#    ## PRINT SCRAPED DATA ##
#    s  = '***'
#    s0 = '\n'+s
#    d  ='#---------------------------------------------------------------------------#'
#    dd ='#===========================================================================#'
#    print(f'\n{d}\n {page_url} \n{d}')                          # page_url (str)
#    print(f'{s} publish date (text) {s}:\n    {dt_pub}')        # dt_pub (str)
#    print(f'{s0} author name (text) {s}:\n    {auth_name}')     # auth_name (str)
#    print(f'{s0} author profile (text) {s}:\n    {auth_url}')   # auth_url (str)
#    print(f'{s0} header (text) {s}:\n    {header}')             # header (str)
#    print(f'{s0} header img url (text) {s}:\n    {img_header_url}')     # img_header_url (str)
#    print(f'{s0} header img author (text) {s}:\n    {img_header_auth}') # img_header_auth (str)
#    body_print = f"{body[:75]} ... {body[-75:]}" if DEBUG_HIDE else body
#    print(f'{s0} body (text) {s}: -> DEBUG_HIDE={DEBUG_HIDE}\n    {body_print}') # body (str)
#    print(f'{s0} article imgs (list text x{len(lst_art_imgs)}) {s}:\n    {json.dumps(lst_art_imgs, indent=4)}') # lst_art_imgs (lst)
#    print(f'{s0} article img authors (list text x{len(lst_art_img_auths)}) {s}:\n    {json.dumps(lst_art_img_auths, indent=4)}') # lst_art_img_auths (lst)
#    print(f'{s0} body query (text, i.e. search article for country or company name) {s}:\n    n/a') # ?
    
    # RETURN SCRAPED DATA DICT
    #return {'page_url':page_url, 'dt_pub':dt_pub, 'auth_name':auth_name, 'auth_url':auth_url, 'header':header, 'img_header_url':img_header_url, 'img_header_auth':img_header_auth, 'body':body, 'lst_art_imgs':lst_art_imgs, 'lst_art_img_auths':lst_art_img_auths}

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
    if WRITE_CSV: write_lst_dict_to_csv(LST_CSV_EXPORT, 'TEST_SILK_OUTPUT.csv')
    

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

