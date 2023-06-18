#!/usr/bin/env python
__filename = 'test_abe.py'
__fname = 'test_abe'
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
#from lxml.html import fromstring
from lxml import html
#import requests
from googletrans import Translator
#from translate import Translator
from bs4 import BeautifulSoup
from selenium import webdriver # pip install -U selenium
#from selenium.common.exceptions import WebDriverException
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
HTML_1 = importlib.import_module('03_test_abe_html_1')
HTML_2 = importlib.import_module('03_test_abe_html_2')

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
WAIT_TIME = 10 # sec
WR_HI = 0
WR_LOW = -5

LOCAL_TEST = False
LST_PG_URLS = [ # GET https://www.target.com/s?searchTerm=airpods+pro
    "https://www.target.com/p/apple-airpods-pro-2nd-generation/-/A-85978612#lnk=sametab",
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
#        driver.get(page_url) # gen html obj from webdriver's html src str
#        html_cont = html.fromstring(driver.page_source)
#        html_cont_str = driver.page_source
        
#        html_cont_int = html.fromstring(driver.page_source)

        # Explicitly wait for the presence of an element on the page
        #   note_061823: GUI tab 'Shipping & Returns', needs click
        #    in order to render 'Shipping details' & 'Return details' (scraped below)
        wait = WebDriverWait(driver, 30)  # Maximum wait time of 10 seconds
        driver.get(page_url) # gen html obj from webdriver's html src str
        el = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='tab-ShippingReturns']")))
        el.click()
#        wait.until(EC.element_to_be_clickable((By.XPATH, "//li//a[contains(@href, '#tabContent-tab-ShippingReturns')]"))).click()
#        driver.find_element(By.XPATH, "//a//div[contains(text(), 'Shipping &amp; Returns')]").click()
        
        #element = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, 'your_selector'))
#        #xpath_find = "//div//div//div//div//div//div//div//div//div//div//div//picture//img/@src" # @src returns [Object Attr]
#        xpath_find = "//div//div//div//div//div//div//div//div//div//div//div//picture//img" # //img returns element
#        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_find)))
#        element = wait.until(EC.presence_of_element_located((By.XPATH, "//div//h4[contains(text(), 'Shipping details')]")))
        
        
        html_cont = html.fromstring(driver.page_source)
        html_cont_str = driver.page_source
        
#        "//div//div//div//h4[contains(text(), 'Description')]"
#
#        )[0]
#        child_div.xpath(".//div//div//div//div//div//div//div//picture//img/@src")[0]
            #ref: https://www.selenium.dev/selenium/docs/api/py/_modules/selenium/webdriver/common/by.html#By
            #ref: https://github.com/SeleniumHQ/selenium/blob/a4995e2c096239b42c373f26498a6c9bb4f2b3e7/py/CHANGES
            #ref: https://stackoverflow.com/a/72773269/2298002
            #"""Set of supported locator strategies."""
            #ID = "id"
            #XPATH = "xpath"
            #LINK_TEXT = "link text"
            #PARTIAL_LINK_TEXT = "partial link text"
            #NAME = "name"
            #TAG_NAME = "tag name"
            #CLASS_NAME = "class name"
            #CSS_SELECTOR = "css selector"
            
#            CLIENT.find_element(By.CSS_SELECTOR, ".cl-goto-post").click()
#            sel_menu_els = CLIENT.find_elements(By.CSS_SELECTOR, ".ui-selectmenu-text")
#
#            elements = CLIENT.find_elements(By.NAME, "id")
#            elements = CLIENT.find_elements(By.CSS_SELECTOR, ".ui-state-default")
#            text = elements[i].text
#
#            CLIENT.find_element(By.ID, "PostingBody").send_keys(str_i_3)
#            CLIENT.find_element(By.NAME, "price").send_keys(str_i_4)
#
#            sel_menu_els = CLIENT.find_elements(By.CSS_SELECTOR, ".ui-selectmenu-text")
#            sel_menu_els[i].click()
#
#            sel_menu_el_par = sel_menu_els[i].find_element(By.XPATH, "..")
#            sel_menu_el_par_id = sel_menu_el_par.get_attribute("id")
#            if sel_menu_el_par_id == 'ui-id-1-button':
    else:
#        html_cont = html.fromstring(HTML_1.TEST_HTML) # from 03_test_abe_html_1.py
        html_cont = html.fromstring(HTML_2.TEST_HTML) # from 03_test_abe_html_2.py
        html_cont_str = driver.page_source
        driver.quit()
    
#    # print OG html version
#    print(f"\n\n _ html_cont (OG) _ \n{html_cont_str}")
#    print('*** break point ***')
#    while True: pass

    ## retrieve product image asset urls ##
    # <button><div><div><div><picture><img src='...'>
    lst_img_src = html_cont.xpath("//button//div//div//div//picture//img/@src")
        
    ## get 'Highlights' bullet points ##
    # only select the text nodes of <span> elements that have direct text content.
    #   filters empty or whitespace-only text nodes)
    lst_span_text = html_cont.xpath("//ul//div//div//li//span/text()")
    
    # retrieve all text, including both direct & nested text content
    #   use: descendant-or-self::text() axis
    #lst_span_text = driver.xpath("//ul//div//div//li//span//descendant-or-self::text()")
    #lst_span_text = [text.strip() for text in lst_span_text if text.strip()] # filter empty or whitespace-only text nodes

    ## get 'Specifications' key/values ##
    dict_specs = {}
#    lst_h4_tags     = driver.find_elements_by_xpath("//div//div//div//h4[contains(text(), 'Specifications')]")
    lst_h4_tags     = html_cont.xpath("//div//div//div//h4[contains(text(), 'Specifications')]")
    div_par         = lst_h4_tags[0].getparent()
    lst_childs      = div_par.getchildren()
    lst_div_childs  = [child for child in lst_childs if child.tag == 'div']
        # lst_div_childs[0] = <div> <div><b>key</b>val</div> </div>
    for idx, child in enumerate(lst_div_childs):
        if child.tag == 'div':
            b_tag = child.getchildren()[0]
            str_val = child.text_content().strip()
            dict_specs[b_tag.text_content()] = str_val
            
#        print('child.tag: '+child.tag)
#        [print('child_1 <div> tag: '+child_1.tag) for child_1 in child.getchildren() if child_1.tag == 'div']
#        [print('child_1 <b> tag: '+child_1.tag) for child_1 in child.getchildren() if child_1.tag == 'b']
#        # get <div> tags in this iteration (should just be one)
#        #lst_div_childs_1 = [child_1 for child_1 in child.getchildren() if child.tag == 'div']
#        tag_div = [child_1 for child_1 in child.getchildren() if child_1.tag == 'div'][0]
#        tag_b = [child_1 for child_1 in child.getchildren() if child_1.tag == 'b'][0]
#
#        # from the 1st <div>, get the 1st <b>
##        tag_b = child.getchildren()[0]
#        dict_specs[tag_b.text_content()] = tag_div.text_content()
        
    ## get 'Description' text ##
    str_descr_html = ''
    lst_h4_tags     = html_cont.xpath("//div//div//div//h4[contains(text(), 'Description')]")
    [print(f'tag: {v} _ text_content: {v.text_content()}') for v in lst_h4_tags]
    div_par         = lst_h4_tags[0].getparent()
    print(f'div_par: {div_par}')
    lst_childs      = div_par.getchildren()
    [print(f'tag: {v} _ text_content: {v.text_content()}') for v in lst_childs]
    lst_div_childs  = [child for child in lst_childs if child.tag == 'div']
        # lst_div_childs[0] = <div> text<br>text<br>... </div>
#    str_descr_html = lst_div_childs[0].get_attribute('innerHTML')
    # Get the inner HTML of the div_par element
#    inner_html = html.tostring(div_par, encoding='unicode')
#    str_descr_html = html.tostring(lst_div_childs[0], encoding='unicode')
    str_descr_html = lst_div_childs[0].text_content()
    
    ## get 'Description' key/values & images ##
#    dict_descr = {}
    lst_descr_imgs = []
#    for idx, child_div in enumerate(lst_div_childs[1:]):
    print(f'len(lst_div_childs): {len(lst_div_childs)}')
    [print(f'div: {v}') for v in lst_div_childs]
    [print(f'div: {v}') for v in lst_div_childs[1:]]
    div_par_par = div_par.getparent()
    lst_div_childs  = [child for child in div_par_par.getchildren() if child.tag == 'div']
    div_tag = lst_div_childs[2]
#    lst_div_tags = div_tag.xpath(".//div//div//div").getchildren()
#    lst_div_tags = [child for child in div_tag.xpath(".//div//div//div").getchildren() if child.tag == 'div']
    lst_div_tags = [child for child in div_tag.xpath(".//div//div//div//div") if child.tag == 'div']
    
#    lst_div_tags = html_cont.xpath(".//div//div//div//div[@data-test='wellnessBadgeAndDescription']")
    lst_div_tags = html_cont.xpath(".//div[@data-test='wellnessBadgeAndDescription']")
#    data-test="wellnessBadgeAndDescription"
#    print(f'\nlen(lst_div_tags): {len(lst_div_tags)}')
#    [print(f'div: {v}') for v in lst_div_tags]
#    [print(f'div: {v}') for v in lst_div_tags[1:]]
    
    
#    lst_div_childs = div_tag.getchildren()
#    str_img_url = div_tag.xpath("//div//div//div//div//div//div//div//div//picture//img/@src")[0]
#    str_img_url = div_tag.xpath("//div//div//div//div//div//div//div//div//picture//img/@src")[0]
    
#    for idx, div in lst_div_tags:
    print(f'len(lst_div_tags) -> {len(lst_div_tags)}')
    for idx in range(0, len(lst_div_tags), 1):
        print(f'\nidx: {idx} of {len(lst_div_tags)-1}')
#        if idx > len(lst_div_tags)-2: continue
        
#        div_childs = lst_div_tags[idx].getchildren()
        div_w_img = lst_div_tags[idx].getchildren()[0]
        div_w_text = lst_div_tags[idx].getchildren()[1]
#        div_w_text = lst_div_tags[idx+1]
        
        print(f'trying 5 divs... idx: {idx}')
#        img_xpath = "//div//div//div//div//div//picture//img/@src" # handle 5 divs
#        lst_imgs = div_w_img.xpath('.'+img_xpath)
#        lst_imgs = div_w_img.xpath(".//div//div//div//div//div//picture//img/@src")
        lst_imgs = div_w_img.xpath(".//picture//img/@src")
#        if len(lst_imgs) == 0: # handle 6 divs
#            print(f'using 6 divs... idx: {idx}')
#            #lst_imgs = div_w_img.xpath('.//div'+img_xpath)
#            lst_imgs = div_w_img.xpath(".//div//div//div//div//div//picture//img/@src")
        str_img_url = lst_imgs[0]
        print('str_img_url: '+ str_img_url)
        
        str_key = div_w_text.xpath(".//div/text()")[0]
#        str_key = div_w_text.xpath(".//div//div/text()")[0]
#        str_key = div_w_text.xpath("./text()")[0]
#        str_key = div_w_text.text_content()
        print('str_key: '+ str_key)
        
        str_val = div_w_text.text_content().replace(str_key, '').strip()
#        str_val = div_w_text.text_content()
        print('str_val: '+ str_val)
        
#        dict_descr[str_key] = str_val
#        lst_descr_imgs.append(str_img_url)
        lst_descr_imgs.append({str_key:{'img_url':str_img_url, 'descr':str_val}})
        
#    for idx, child_div in enumerate(lst_div_tags):
##        str_img_url = child_div.xpath(".//div//div//div//div//div//picture//img/@src")[0]
#        img_xpath = "//div//div//div//div//div//picture//img/@src"
#        lst_imgs = child_div.xpath('.'+img_xpath)
#        if len(lst_imgs) == 0:
#            lst_imgs = child_div.xpath('.//div'+img_xpath)
#
#        str_img_url = lst_imgs[0]
#        print('str_img_url: '+ str_img_url)
##        str_img_url = html_cont.xpath("//div//div//div//div//div//div//div//picture//img/@src")[0]
#        str_key = child_div.xpath(".//div/text()")[0] # Find the child <div> elements within the parent
#        print('str_key: '+ str_key)
##        str_val = child_div.xpath("./text()")[0]
#        str_val = child_div.text_content().replace(str_key, '')
#        print('str_val: '+ str_val)
#
##        str_key = child_div.xpath(".//div//div//div/text()")[0] # Find the child <div> elements within the parent
#
#        # should maintain key/val -> idx in sync
#        dict_descr[str_key] = str_val
#        lst_descr_imgs.append(str_img_url)
        
    
    ## get 'Shipping details' & 'Return details' key/vals ##
#    dict_ship = dict_ret = {}
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
#    print(f'{s0} Description (key/vals) {s}:\n{json.dumps(dict_descr, indent=4)}') # descr key/vals
    print(f'{s0} Description (list key/vals) {s}:\n{json.dumps(lst_descr_imgs, indent=4)}') # descr imgs
    
    print(f'\n{d}\nSHIPPING & RETURNS\n{d}')
    print(f'{s} Shipping details (key/vals) {s}:\n{json.dumps(dict_ship, indent=4)}') # ship details key/vals
    print(f'{s0} Return details (key/vals) {s}:\n{json.dumps(dict_ret, indent=4)}') # return details key/vals
#    # parse out article descr & body text
#    print('\nParsing "description" & "body"...')
#    idx_start = html_cont.index('"description":"')+len('"description":"')
#    idx_end = html_cont[idx_start:].index('"')
#    descr = html_cont[idx_start:idx_start+idx_end+1]
#    print('\nDESCR:\n '+descr)
#
#    idx_start = html_cont.index('"articleBody":"')+len('"articleBody":"')
#    idx_end = html_cont[idx_start:].index('"')
#    body = html_contt[idx_start:idx_start+idx_end+1]
#    print('\nBODY:\n '+body)

    # print OG html version
    #print(f"\n\n _ html_cont (OG) _ \n{html_cont}")
    
    # translate html_cont from french to english (fr -> en)
    #translator = Translator(service_urls=['translate.google.com'])
    #html_cont_trans = translator.translate(html_cont, src='fr', dest='en').text

    # print TRANS html version
    #print(f"\n\n _ html_cont (TRANS) _ \n"+html_cont_trans)

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



