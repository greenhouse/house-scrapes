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
#from googletrans import Translator
from translate import Translator
import time
from lxml.html import fromstring
from datetime import datetime

## automation requirements ##
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup # python3.7 -m pip install bs4

## chrome browser web driver ##
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

## tor browser web driver ##
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

#------------------------------------------------------------#
#   BROWSER DRIVER (CHROME/TOR)                              #
#------------------------------------------------------------#
# default: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
NEW_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36"
MASK_UA = False
CHECK_UA = True

CHROME = True
TOR = False
FIRE = False
SAFARI = False

print(f'\n\n... running ...\n _ CHROME: {CHROME}\n _ TOR: {TOR}\n _ FIRE: {FIRE}\n _ SAFARI: {SAFARI} ...')
print(f'... user-agent ...\n _ MASK_UA: {MASK_UA}\n _ CHECK_UA: {CHECK_UA}\n ...\n\n')

if CHROME: # init options w/ chrome driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    #options.add_argument('--remote-debugging-port=9222') # trying to use existing chrome isntance

    if MASK_UA: options.add_argument(f'user-agent={NEW_UA}')
    
    # init chrome driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options) # chrome browser

    # init chrome driver w/ service (receiving error about chromedriver version)
    #driver_service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=driver_service, options=options)
    
    # init chrome driver w/ custom path
    #chromedriver_path = '/usr/local/bin/chromedriver'  # Adjust the path accordingly
    #driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    
    '''
    note_061623_2023:
        1) it appears that launching browsers through code, leads to a 'banned' message
        2) but using my regular GUI browser (not launching through code)
            seems to still work just fine without a ban
        3) this leads me to believe that my IP is not actually banned
    '''
    
elif TOR: # init options w/ tor driver
    options = Options() #  set Firefox options Tor Browser
    options.binary_location = '/Applications/Tor Browser.app/Contents/MacOS/firefox' # path to browser executable
    #options.add_argument('--proxy-server=socks5://127.0.0.1:9050')  # attempting auto-connect to Tor on localhost port 9050
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.set_preference('permissions.default.image', 2) # disable loading images
    if MASK_UA: options.add_argument(f'user-agent={NEW_UA}')
    
    # Set Browser service executable
    tor_browser_service = Service('/Applications/Tor Browser.app/Contents/MacOS/geckodriver')
    
    # init tor driver
    driver = webdriver.Firefox(service=tor_browser_service, options=options) # w/ tor browser service
    
elif FIRE: # init options w/ firefox driver
    options = webdriver.FirefoxOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.set_preference('permissions.default.image', 2) # disable loading images
    if MASK_UA: options.add_argument(f'user-agent={NEW_UA}')
    
    # init firefox driver
    driver = webdriver.Firefox(options=options)

elif SAFARI:
    ## NOTE_061623: no Selenium 'options' for Safari (not like Chrome or Firefox/Tor does) ##
    #options = webdriver.SafariOptions()
    #options = Options() #  set Firefox options Tor Browser
    #options.add_argument('--disable-blink-features=AutomationControlled')
    #options.set_preference('permissions.default.image', 2) # disable loading images
    #options.page_load_strategy = 'eager'  # Set the page load strategy
    #options.add_argument('--private')  # Open Safari in private browsing mode
    #options.add_argument('--start-fullscreen')  # Start Safari in fullscreen mode
    #if MASK_UA: options.add_argument(f'user-agent={NEW_UA}')
    
    # init firefox driver
    safari_driver_path = '/usr/bin/safaridriver'
    driver = webdriver.Safari(executable_path=safari_driver_path)
    #driver = webdriver.Safari(executable_path=safari_driver_path, options=options)
    
else:
    print('\n\n*** ERROR *** _ no browser driver selected _ exiting...\n\n')
    exit(0)

# check current user agent
if CHECK_UA:
    user_agent = driver.execute_script("return navigator.userAgent;")
    print(f"\nCurrent user-agent:\n {user_agent}\n")
    #while True: pass # halt script

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
#ref: https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=2
root_uri = 'https://www.coursesu.com'
search_uri = '/c/charcuterie-traiteur/charcuterie/jambon-blanc'
search_uri_p = root_uri + search_uri + '?page='
curr_pg_num = '10'
sleep_cnt = 0

GO_TIME_START = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
print(f'\n\nGO_TIME_START: {GO_TIME_START}\n')

def get_time_now():
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
while True: # loop until tor browser gets the site
    try:
        driver.get(search_uri_p + curr_pg_num)
        print(" ... browser 'get' initial site page has been completed\n")
        break
    except WebDriverException as e:
        #print(f"*** EXCEPTION *** _ e:\n {e}"))
        print(f"*** EXCEPTION *** _ e: (silenced; waiting for 'get({search_uri_p + curr_pg_num})' to complete...")
        time.sleep(10)

while True: # loop until captcha no longer found on page
    try:
        #print("try: driver.find_element(...)")
        #driver.find_element(By.XPATH, "//iframe[@id='main-iframe']")
        
        print("Looking for captcha source code ...")
        driver.find_element(By.XPATH, "//iframe[@onload='iframeOnload()']")
        print(f"Waiting for user captcha to be solved ... sleep(5) ... sleep_tot({(sleep_cnt+1) * 5})")
        time.sleep(5)
        sleep_cnt+=1
    except Exception as e:
        print(f"\n** WANRING ** _ no captcha source code found... manual solve complete?\n")
        #print(f"\n** EXCEPTION ** _ element not found _ e:\n{e}\n _ e _ DONE\n")
        break
                
sleep_cnt = 0
while True: # loop through until coockie accept button is auto-clicked
    try:
        driver.find_element(By.XPATH, "//button[@id='popin_tc_privacy_button_2']").click()
        print(' ... cookie accept button has been auto-clicked')
        break
    except WebDriverException as e:
        #print(f"*** EXCEPTION *** _ e:\n {e}"))
        print(f"*** EXCEPTION *** _ e: (silenced; waiting for cookie accept button to load & then auto-click...")
        time.sleep(5)
    
# get links to all items on this page number
html = fromstring(driver.page_source)
links_pg_items = html.xpath("//a[@class='product-tile-link']/@href")

found_end = False
pg_item_links_done = []
pg_item_links_img_none = []
print(f"\n\n ... STARTING INITIAL PAGE #{curr_pg_num}\n ...  {search_uri_p + curr_pg_num}\n")

while not found_end:
    # loop through items on this page number
    print(f"\nSTARTING PAGE #{curr_pg_num} _ looping through 'links_pg_items'")
    print(f'links_pg_items cnt: {len(links_pg_items)}')
    for idx,link in enumerate(links_pg_items):
        print(f"{idx}: {link}")
        
        # get html for this item link
        driver.get(root_uri + link)
        html_content = fromstring(driver.page_source)
        
        # translate html_content from french to english (fr -> en)
        translator = Translator(service_urls=['translate.google.com'], to_lang='en')
        #html_x = translator.translate(html_content, src='fr', dest='en').text
        html_x = translator.translate(html_content, dest='en').text
        
        
        ## TODO: 061523 ... left off here: need finish testing 'ingredients' & 'nutrional values' ##
        print('    url: '+link)
        print('    collected_at: '+get_time_now())

        # get ingredients (Ingrédients)
        #lst_h3 = html_x.xpath("//h3[contains(text(), 'Ingrédients')]/text()")
        #lst_h3 = html_x.xpath("//h3[contains(text(), 'ingredients')]")
        #lst_h3 = html_x.xpath("//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = 'ingredients']")
        #lst_h3 = html_x.xpath("//h3[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = 'Ingrédients']")
        lst_h3 = html_x.xpath("//h3[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = 'ingredients']")
        li_parent = lst_h3[0].getparent()
        ul_parent = li_parent.getparent()
        lst_childs = ul_parent.getchildren()

        lst_li_childs = [child for child in lst_childs if child.tag == 'li']
        for idx, child in enumerate(lst_li_childs):
            if child.getchildren()[0].tag == 'h3':
                print(child.tag)
                h3_child = child.getchildren()[0]
                
                # get ingredients (Ingrédients)
                if h3_child.text_content() == 'ingredients' or h3_child.text_content() == 'Ingrédients':
                    print(h3_child.text_content())
                    p_child = lst_li_childs[idx+1].getchildren()[0]
                    print('Ingredients: '+p_child.text_content())
                
                # get nutrional values (valeurs_nutritionnelles)
                if h3_child.text_content() == 'nutrional values' or h3_child.text_content() == 'Valeurs nutritionnelles':
                    print(h3_child.text_content())
                    p_child = lst_li_childs[idx+1].getchildren()[0]
                    print('Nutrional Values: '+p_child.text_content())
        ## TODO: 061523: need finish testing 'ingredients' & 'nutrional values' ##
        
        # get imge for this item
        link_imgs = html_x.xpath("//picture//img/@src")
        print(f'    link_imgs cnt: {len(link_imgs)}')
        if len(link_imgs) > 0:
            print(f"    img 0: {link_imgs[0][:50]}...{link_imgs[0][-25:-1]}")
        else:
            pg_item_links_img_none.append(link) # track item links with no image
        pg_item_links_done.append(link) # track finished item links
        
        wait_sec = 1
        print(f'    wait sec... {wait_sec}\n')
        time.sleep(wait_sec)
        
        print("\n\n*** BREAK POINT *** _ PAUSE EXECUTION & MAINTAIN BROWSER OPEN ....\n\n")
        while True: pass
        
    # check if this page number text triggers no more items ('Fin de liste')
    lst_pg_end_trig = html.xpath("//p[contains(text(), 'Fin de liste')]/text()")
    print("\n\n ** lst_pg_end_trig **:\n", *lst_pg_end_trig, sep='\n')
    lst_blocked_trig = html.xpath("//title[contains(text(), 'You have been blocked')]/text()")
    print("\n\n ** lst_blocked_trig **:\n\n", *lst_blocked_trig, sep='\n')
    #if len(lst_pg_end_trig) > 0:
    if len(lst_pg_end_trig) > 0 or len(lst_blocked_trig) > 0:
        # 061223_2240: check for website block (appears to happen after 7 minutes of running
        if len(lst_blocked_trig) > 0:
            print("** WARNING ** _ FOUND BLOCKED TRIGGER: 'You have been blocked'\n ... attempting to proceed as if nothing is wrong :O")

        # print current status
        next_pg_num = str(int(curr_pg_num) +1)
        print(f"\n\n ... FINISHED PAGE #{curr_pg_num}\n ... STARTING PAGE #{next_pg_num}\n ...  {search_uri_p + next_pg_num}\n")
                
        # get next search result page number
        curr_pg_num = next_pg_num
        driver.get(search_uri_p + curr_pg_num)
        
        # get links to all items for this new page number
        prev_pg_item_cnt = len(links_pg_items)
        html = fromstring(driver.page_source)
        links_pg_items = html.xpath("//a[@class='product-tile-link']/@href")
        
        # compensate for the site including previous items
        #   note: driver.get() returns previous page items along with designated '?page=X'
        #       instead of only providing items from designated '?page=X'
        #   fix: need to remove previous pages items from links_pg_items,
        #       by comparing duplicates against 'pg_item_links_done'
        links_pg_items = [item for item in links_pg_items if item not in pg_item_links_done]
        
        CURR_TIME = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
        print(f'\n ... CURR_TIME: {CURR_TIME}\n')
    else:
        
        # check if captcha was found,
        #   if not: exception will raise maintaining 'found_captcha = False'
        #       resulting final prints to occur (not 'continue' parent loop)
        #   if yes: enter loop to wait for user to solve captcha manually
        #       leading to exception raised w/ 'found_captcha = True'
        #       resulting in 'continue' parent loop w/ 'curr_pg_num' un-changed
        found_captcha = False
        while True: # loop until captcha no longer found on page
            try:
                print("Looking for captcha source code ...")
                str_text = 'We want to make sure it is actually you we are dealing with and not a robot'
                driver.find_element(By.XPATH, f"//p[contains(text(), '{str_text}')]/text()")
                print(f"Waiting for user captcha to be solved ... sleep(5) ... sleep_tot({(sleep_cnt+1) * 5})")
                time.sleep(5)
                sleep_cnt+=1
                found_captcha = True # trigger captcha found
            except Exception as e:
                #print(f"*** EXCEPTION *** _ e:\n {e}"))
                print(f"\n** WANRING ** _ no captcha source code found... manual solve complete?\n")
                break
        
        # if 'found_captcha', then continue loop with curr_pg_num un-changed
        if found_captcha: continue
        
        print(f"\n\n *** NO MORE PAGE ITEMS LEFT ***:\n last page item -> {idx}: {link}\n search_uri_p -> {search_uri_p+curr_pg_num}\n    ... printing additional info")
        print(f'\n\n** PRINTING ** pg_item_links_done ({len(pg_item_links_done)})...', *pg_item_links_done, sep='\n ')
        print(f'\n\n** PRINTING ** pg_item_links_img_none ({len(pg_item_links_img_none)})...', *pg_item_links_img_none, f'\n ...pg_item_links_img_none ({len(pg_item_links_img_none)}',' ...pg_item_links_done ({len(pg_item_links_done)})', sep='\n ')
        found_end = True
        continue

GO_TIME_END = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
print(f'\n\nGO_TIME_START: {GO_TIME_START}')
print(f'GO_TIME_END:   {GO_TIME_END}')

print("\n\n.... SETTING ENDLESS LOOP TO MAINTAIN BROWSER OPEN ....\n\n")
while True:
    pass
    
#    style="background-image: url("https://www.coursesu.com/dw/image/v2/BBQX_PRD/on/demandware.static/-/Sites-digitalu-master-catalog/default/dw051814d5/3256229544041_A1N1_2511315_S13.png?sw=388&sh=388&sm=fit
    

#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
#   NOWIS OG ATTEMPT (*DO NOT DELETE*)                                                                          #
#---------------------------------------------------------------------------------------------------------------#
#
#
##!/usr/bin/env python
#__filename = 'nowis_cours_scrape.py'
#__fname = 'nowis_cours_scrape'
#cStrDividerExcept = '***************************************************************'
#cStrDivider = '#================================================================#'
#print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
#print(f'GO {__filename} -> starting IMPORTs and globals decleration')
#
##------------------------------------------------------------#
##   IMPORTS                                                  #
##------------------------------------------------------------#
#import sys, argparse, string, ctypes, os, re
#import time
#from datetime import datetime
#import requests
#from googletrans import Translator
##from translate import Translator
#from bs4 import BeautifulSoup
#from selenium import webdriver # pip install -U selenium
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#    #from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#    #from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#    #from selenium.webdriver.firefox.options import Options
#
##------------------------------------------------------------#
##   GLOBALS                                                  #
##------------------------------------------------------------#
#WAIT_TIME = 60 # sec
##WAIT_TIME = 60 * 60 # 1 hr
#
#LST_PG_URLS = [
#    "https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=1",
#    "https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=2"
#]
#
##------------------------------------------------------------#
##   PROCEDURAL SUPPORT                                       #
##------------------------------------------------------------#
#def scrape_target_pg(page_url : str):
#    ## Selenium: init webdrive ##
#    print(f'\nInitializing Selenium webdrive...')
#
#    # Configure Selenium options
#    options = Options()
#    options.add_argument("--headless")  # Run Chrome in headless mode
#
#    # Create a new Selenium driver
#    #driver = webdriver.Firefox(options=options) # eg_051723: firefox taking 30sec+
#    driver = webdriver.Chrome(options=options)
#
#    ## Selenium: retreive html_content ##
#    req_time_start = datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#    driver.get(page_url)
#    html_content = driver.page_source
#
#    # translate html_content from french to english (fr -> en)
#    translator = Translator(service_urls=['translate.google.com'])
#    html_content_trans = translator.translate(html_content, src='fr', dest='en').text
#
#    # print both OG & TRANS versions
#    print(f"\n\n _ html_content (OG) _ \n{html_content}")
#    print(f"\n\n _ html_content (TRANS) _ \n"+html_content_trans)
#
#    print(f'\n\n scraping {page_url} _ DONE _')
#
#def get_time_now():
#    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
#
#def exe_pg_scrape_loop(lst_pgs : lst, wait_sec : float):
#    for pg_url in lst_pgs:
#        go_time_start = get_time_now()
#        print(f'pg scrape start: {go_time_start}')
#
#        scrape_target_pg(pg_url)
#
#        print(f'pg scrape start: {go_time_start}')
#        print(f'pg scrape end:   {get_time_now()}')
#
#        if wait_sec > 0:
#            print(f'wait sec... {wait_sec}')
#            time.sleep(wait_sec)
#
##------------------------------------------------------------#
##   DEFAULT SUPPORT                                          #
##------------------------------------------------------------#
#def go_main():
#    run_time_start = get_time_now()
#    print(f'\n\nRUN_TIME_START: {run_time_start}')
#    read_cli_args() # print cli args
#    argCnt = len(sys.argv) # get arg cnt
#
#    # validate args
#    if argCnt > 1:
#        print('*** ERROR *** _ invalid args\n ... exiting\n\n')
#        exit(1)
#
#    # loop through and scrape each url
#    exe_pg_scrape_loop(LST_PG_URLS, WAIT_TIME)
#
#    print(f'\n\nRUN_TIME_START: {run_time_start}')
#    print(f'RUN_TIME_END:   {get_time_now()}')
#
#def read_cli_args():
#    funcname = f'<{__filename}> _ ENTER _ read_cli_args'
#    print(f'\n{funcname}...')
#    argCnt = len(sys.argv)
#    print(' # of args: %i' % argCnt)
#    print(' argv lst: %s' % str(sys.argv))
#    for idx, val in enumerate(sys.argv):
#        print(f' argv[{idx}]: {val}')
#    print(f'DONE _  read_cli_args...')
#
#if __name__ == "__main__":
#    go_main()
#
##ref: https://www.selenium.dev/selenium/docs/api/py/_modules/selenium/webdriver/common/by.html#By
##ref: https://github.com/SeleniumHQ/selenium/blob/a4995e2c096239b42c373f26498a6c9bb4f2b3e7/py/CHANGES
##ref: https://stackoverflow.com/a/72773269/2298002
#"""Set of supported locator strategies."""
##ID = "id"
##XPATH = "xpath"
##LINK_TEXT = "link text"
##PARTIAL_LINK_TEXT = "partial link text"
##NAME = "name"
##TAG_NAME = "tag name"
##CLASS_NAME = "class name"
##CSS_SELECTOR = "css selector"
#
#
#
