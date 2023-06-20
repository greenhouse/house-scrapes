#!/usr/bin/env python
__filename = 'gun_mbay_demo.py'
__fname = 'gun_mbay_demo'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
from gun_support import * # sys, os, re, json
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
HTML_x = importlib.import_module('04_test_gun_html_2')

#------------------------------------------------------------#
#   GLOBALS                                                  #
# GET https://news.mongabay.com/?s=illegal+logging
#------------------------------------------------------------#
WAIT_TIME = 10 # sec
WR_HI = 0
WR_LOW = -5
#AUTO_CLICK_WAIT = False
LOCAL_TEST = False
DEBUG_HIDE = True
WRITE_CSV = False
LST_PG_URLS = [ # GET https://news.mongabay.com/?s=illegal+logging
    "https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/", # OG
    "https://news.mongabay.com/2022/09/illegal-logging-and-trade-in-fine-wood-threaten-wampis-communities-in-the-peruvian-amazon/",
    "https://news.mongabay.com/2022/05/chinese-companies-linked-to-illegal-logging-and-mining-in-northern-drc/", # ALT_1
    "https://news.mongabay.com/2022/03/a-community-in-mexico-reforests-its-land-against-the-advance-of-illegal-logging/"
]
LST_CSV_EXPORT = []

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
def scrape_target_pg(driver, page_url : str):
    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
    print(  f'\nGetting page_url content... w/ GLOBALS (',
            f'\n LOCAL_TEST: {LOCAL_TEST},',
            f'\n DEBUG_HIDE: {DEBUG_HIDE},',
            f'\n WRITE_CSV: {WRITE_CSV},',
            f'\n WAIT_TIME: {WAIT_TIME+WR_LOW} to {WAIT_TIME+WR_HI} sec',
            f'\n)\n', sep='')
            
    if not LOCAL_TEST:
        # auto-click w/ 'immediate click'
        driver.get(page_url) # GET html page
                
        # gen html obj from webdriver's html src str
        hc = html.fromstring(driver.page_source)
        html_cont_str = driver.page_source
    else:
        hc = html.fromstring(HTML_x.TEST_HTML) # from 04_test_gun_html_1.py
        html_cont_str = HTML_x.TEST_HTML
        driver.quit()
    
    # print OG html version
    #print(f"\n\n _ html_cont (OG) _ \n{html_cont_str}")
    #print('*** break point ***')
    #while True: pass
    
    ## get source (organisation/ publisher) ##
    # source (organisation/ publisher) -> '© 2023 Copyright Conservation news': news.mongabay.com
    str_source = 'news.mongabay.com -> © 2023 Copyright Conservation news'

    ## NOTE_061923: detect this article's html layout type (2 article types found/parsed so far)
    '''
        OG article source html code layout (example)
          https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/
        ALT_1 soure html layout (example)
          https://news.mongabay.com/2022/05/chinese-companies-linked-to-illegal-logging-and-mining-in-northern-drc/
    '''
    ## get auth_name & dt_pub -> "//div[@class='single-article-meta' and contains(text(), 'by')]"
    #   "by <a href="https://news.mongabay.com/by/hans-nicholas-jong/">Hans Nicholas Jong</a> on 21 March 2023"
    str_xp = "//div[@class='single-article-meta' and contains(text(), 'by')]" # auth_name & dt_pub support
    str_by = hc.xpath(str_xp)[0].text_content() if len(hc.xpath(str_xp)) > 0 else ''
    if len(str_by) > 0: # detect OG article code layout
        lst_head = [] # misc DEBUG_HIDE support
        
        ## get auth_name & dt_pub -> "//div[@class='single-article-meta' and contains(text(), 'by')]"
        str_on = str_by[str_by.find('by')+2:str_by.find('jQuery')].strip()
        auth_name = str_on.split(' on ')[0].strip()
        dt_pub = str_on.split(' on ')[1].strip()
        
        ## get header -> "//div[@class='article-headline']//h1/text()"
        header = hc.xpath("//div[@class='article-headline']//h1/text()")[0]
        
        ## get auth_url -> "//div[@class='single-article-meta' and contains(text(), 'by')]//a"
        tag_a = hc.xpath("//div[@class='single-article-meta' and contains(text(), 'by')]//a")[0]
        auth_url = tag_a.get('href')

        ## get image header -> "//div[@class='col-lg-12']/@style"
        #   <div class="col-lg-12" style="background: url('https://imgs.mongabay.com/.../kalteng_0235.jpg');background-size: cover; background-position: center">
        s = hc.xpath("//div[@class='col-lg-12']/@style")[0]
        img_header_url = s[s.find("https"):s.find("');")]
        
        ## image author -> "//em[contains(text(), 'Banner image:')]" & "//figcaption[@class='wp-caption-text']"
        img_header_auth = hc.xpath("//em[contains(text(), 'Banner image:')]")[0].text_content()

    else: # default to ALT_1 article code layout
        ## get header, auth_name, dt_pub -> "//div[@class='featured-article-meta']//text()"
        lst_head = [x for x in hc.xpath("//div[@class='featured-article-meta']//text()") if x.strip() != '']
        header = lst_head[0]+'\n'+lst_head[1].strip('\n')
        auth_name = lst_head[3]
        dt_pub = lst_head[4].split('on')[1].strip()
        
        ## get auth_url -> "//span[@class='featured-article-publish']//a/@href"
        auth_url = hc.xpath("//span[@class='featured-article-publish']//a/@href")[0]

        ## get image header -> "//div[@class='col-lg-12 parallax-section full-height article-cover']/@data-image-src"
        img_header_url = hc.xpath("//div[@class='col-lg-12 parallax-section full-height article-cover']/@data-image-src")[0]
        
        ## get image author -> "//em[contains(text(), 'Banner image:')]" & "//figcaption[@class='wp-caption-text']"
        img_header_auth = hc.xpath("//p[contains(text(), 'Banner image:')]")[0].text_content()
        
    # debug print logging
    if not DEBUG_HIDE:
        print(f'lst_head: {lst_head}')
        print(f'auth_name: {auth_name}')
        print(f'auth_url: {auth_url}')
        print(f'dt_pub: {dt_pub}')
        print(f'header: {header}')
        print(f'img_header_url: {img_header_url}')
        print(f'img_header_auth: {img_header_auth}')
    
    ## get body text -> "string(//article)"
    body = hc.xpath("string(//article)").strip()
    body = body[:body.find('Banner image:')]
    body = re.sub(r'\s+', ' ', body).strip() # clean \n
     
    ## article images -> "//figure//img/@class/text()"
    lst_art_imgs = list(hc.xpath("//figure//img/@src"))
    lst_art_img_auths = list(hc.xpath("//figcaption[@class='wp-caption-text']/text()"))

    ## body query (i.e. search article for country or company name) -> ?

    ## PRINT SCRAPED DATA ##
    s  = '***'
    s0 = '\n'+s
    d  ='#---------------------------------------------------------------------------#'
    dd ='#===========================================================================#'
    print(f'\n{d}\n {page_url} \n{d}')                          # page_url (str)
    print(f'{s} publish date (text) {s}:\n    {dt_pub}')        # dt_pub (str)
    print(f'{s0} author name (text) {s}:\n    {auth_name}')     # auth_name (str)
    print(f'{s0} author profile (text) {s}:\n    {auth_url}')   # auth_url (str)
    print(f'{s0} header (text) {s}:\n    {header}')             # header (str)
    print(f'{s0} header img url (text) {s}:\n    {img_header_url}')     # img_header_url (str)
    print(f'{s0} header img author (text) {s}:\n    {img_header_auth}') # img_header_auth (str)
    if DEBUG_HIDE: body = f"{body[:75]} ... {body[-75:]}"
    print(f'{s0} body (text) {s}: -> DEBUG_HIDE={DEBUG_HIDE}\n    {body}') # body (str)
    print(f'{s0} article imgs (list text x{len(lst_art_imgs)}) {s}:\n    {json.dumps(lst_art_imgs, indent=4)}') # lst_art_imgs (lst)
    print(f'{s0} article img authors (list text x{len(lst_art_img_auths)}) {s}:\n    {json.dumps(lst_art_img_auths, indent=4)}') # lst_art_img_auths (lst)
    print(f'{s0} body query (text, i.e. search article for country or company name) {s}:\n    n/a') # ?
    
    
    # RETURN SCRAPED DATA DICT
    return {'page_url':page_url, 'dt_pub':dt_pub, 'auth_name':auth_name, 'auth_url':auth_url, 'header':header, 'img_header_url':img_header_url, 'img_header_auth':img_header_auth, 'body':body, 'lst_art_imgs':lst_art_imgs, 'lst_art_img_auths':lst_art_img_auths}

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
    if WRITE_CSV: write_lst_dict_to_csv(LST_CSV_EXPORT, 'TEST_GUN_OUTPUT.csv')
    

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





