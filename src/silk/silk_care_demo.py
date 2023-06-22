#!/usr/bin/env python
__filename = 'silk_care_demo.py'
__fname = 'silk_care_demo'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
from silk_support import * # sys, os, re, json
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
HTML_x = importlib.import_module('05_test_silk_html_2')

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
LST_PG_URLS = [ # GET https://www.carenity.es/foro/asma-88  (results in list of post links)
    # example post links...
    "https://www.carenity.es/foro/asma/tu-opinion-sobre-los-tratamientos-del-asma/tratamiento-de-las-crisis-de-asma-38588",
    "https://www.carenity.es/foro/asma/tu-opinion-sobre-los-tratamientos-del-asma/inhalador-preventivo-33724",
    "https://www.carenity.es/foro/asma/tu-opinion-sobre-los-tratamientos-del-asma/utilizas-ventolin-32459",
    "https://www.carenity.es/foro/asma/tu-opinion-sobre-los-tratamientos-del-asma/es-posible-curar-el-asma-con-tratamientos-natu-32457"
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
    
    ''' requirements...
        user post elements  user comment data lists
        post_view_cnt
        post_supp_cnt
        post_comm_cnt
        post_headline
        post_usr_img_url    lst_comm_usr_img_urls
        post_un             lst_comm_uns
        post_dt             lst_comm_dts
        post_text           lst_comm_texts
    '''
    
    ## get post_headline -> "//h1[@itemprop='headline']"
    post_headline = hc.xpath("//h1[@itemprop='headline']")[0].text_content()
    
    # get post_usr_img_url & lst_comm_usr_img_urls -> "//div[@class='contribs-item']//p[@class='avatar-container ']//img/@src"
    #   NOTE: returns both post & comment user img urls (post_usr_img_url at idx = 0; comm_usr_img_urls at idx >= 1)
    lst_tags = post_usr_img_url = hc.xpath("//div[@class='contribs-item']//p[@class='avatar-container ']//img/@src")
    post_usr_img_url = lst_tags[0]
    lst_comm_usr_img_urls = lst_tags[1:]

    ## get post_un & lst_comm_uns -> "//p[@onclick='haveToInscription(event); return false;']"
    #   NOTE: returns both post & comment user names (post_un at idx = 0; comm_uns at idx >= 1)
    lst_tags = hc.xpath("//p[@onclick='haveToInscription(event); return false;']")
    lst_uns = [tag.text_content() for tag in lst_tags if not tag.text_content().endswith('\n')]
    post_un = lst_uns[0]
    lst_comm_uns = lst_uns[1:]
    
    ## get post_dt -> <div class="date"> | "//div[@class='date']"
    #   NOTE: returns both post & comment datetime (post_dt at idx = 0; comm_dt at idx >= 1)
    lst_tags = hc.xpath("//div[@class='date']")
    post_dt = lst_tags[0].text_content()
    post_dt = re.sub(r"\s+", " ", post_dt.strip())
    lst_comm_dts = [tag.text_content().strip('\n').strip() for tag in lst_tags[1:]]
    
    ## get post_text & lst_comm_texts -> <div itemprop="text"> | "//div[@itemprop='text']"
    lst_tags = hc.xpath("//div[@itemprop='text']")
    post_text = lst_tags[0].text_content().strip()
    lst_comm_texts = [re.sub(r"\s+", " ", tag.text_content().strip()) for tag in lst_tags[1:]]
    
    # get post_view_cnt, post_supp_cnt, post_comm_cnt -> <ul class="thread-stats"> | "//ul[@class='thread-stats']//li"
    lst_li_tags = hc.xpath("//ul[@class='thread-stats']//li")
    post_view_cnt = lst_li_tags[0].text_content()
    post_supp_cnt = lst_li_tags[1].text_content()
    post_comm_cnt = lst_li_tags[2].text_content()

    ## print OG html version ##
    #print(f"\n\n _ html_cont (OG) _ \n{html_cont_str}")
    #print('*** break point ***')
    #while True: pass
    
    ## PRINT SCRAPED DATA ##
    s  = '***'
    s0 = '\n'+s
    d  ='#---------------------------------------------------------------------------#'
    dd ='#===========================================================================#'
    print(f'\n{dd}\n {page_url} \n{dd}')                                # page_url (str)
    #print(f'\n{d}\n POST & COMMENT DATA \n{d}')
    print(f'\n{d}\n POST DATA \n{d}')
    print(f'{s} post_headline (text) {s}:\n    {post_headline}')        # post_headline (str)
    print(f'{s0} post_un (text) {s}:\n    {post_un}')                   # post_un (str)
    print(f'{s0} post_usr_img_url (text) {s}:\n    {post_usr_img_url}') # post_usr_img_url (str)
    print(f'{s0} post_dt (text) {s}:\n    {post_dt}')                   # post_dt (str)
    print(f'{s0} post_text (text) {s}:\n    {post_text}')               # post_text (str)
    print(f'\n{d}\n COMMENT DATA LISTS \n{d}')
    print(  f'{s} lst_comm_uns (list text x{len(lst_comm_uns)}) {s}:',
            f'{json.dumps(lst_comm_uns, indent=4)}', sep='\n')          # lst_comm_uns (lst)
    print(  f'{s0} lst_comm_usr_img_urls (list text x{len(lst_comm_usr_img_urls)}) {s}:',
            f'{json.dumps(lst_comm_usr_img_urls, indent=4)}', sep='\n') # lst_comm_usr_img_urls (lst)
    print(  f'{s0} lst_comm_dts (list text x{len(lst_comm_dts)}) {s}:',
            f'{json.dumps(lst_comm_dts, indent=4)}', sep='\n')          # lst_comm_dts (lst)
    print(  f'{s0} lst_comm_texts (list text x{len(lst_comm_texts)}) {s}:',
            f'{json.dumps(lst_comm_texts, indent=4)}', sep='\n')        # lst_comm_texts (lst)
    print(f'\n{d}\n POST META DATA \n{d}')
    print(f'{s} post_view_cnt (text) {s}:\n    {post_view_cnt}')       # post_view_cnt (str)
    print(f'{s0} post_supp_cnt (text) {s}:\n    {post_supp_cnt}')       # post_supp_cnt (str)
    print(f'{s0} post_comm_cnt (text) {s}:\n    {post_comm_cnt}')       # post_comm_cnt (str)
    
    # RETURN SCRAPED DATA DICT
    return {'page_url':page_url, 'post_headline':post_headline, 'post_un':post_un, 'post_usr_img_url':post_usr_img_url, 'post_dt':post_dt, 'post_text':post_text, 'lst_comm_uns':lst_comm_uns, 'lst_comm_usr_img_urls':lst_comm_usr_img_urls, 'lst_comm_dts':lst_comm_dts, 'lst_comm_texts':lst_comm_texts, 'post_view_cnt':post_view_cnt, 'post_supp_cnt':post_supp_cnt, 'post_comm_cnt':post_comm_cnt}

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

