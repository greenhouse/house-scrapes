# TARGETS (ABE _ hackerabe)

## gun -> news.mongabay.com
### account log
    - https://news.mongabay.com
        (no account creation required)
        
### goals
    - gunther (disc)
        "Hi there. These would be a list of websites that I would like to crawl for news articles for specific keywords (e.g. illegal logging). From those articles, I want to export: source (organisation/ publisher), date, heading, body text, image, and ideally some information from the body text, i.e. if a certain country or company has been mentionend in the article"
        "that's correct. I want to search for specific keywords/ news topics"

### known bugs
    TODO: :- 04_test_gun.py initial integration attempts (not 100% yet)
        - initial test integration for gunther demo requirements
            scrape 4 sites that results from query: ‘illegal logging’
        - within these 4 test sites…
            found 2 different html content layouts to scrape from
        - this means the current code base successfully demonstrates 
            extracting the same exact data from 2 different 
            rendered layouts provided by the same server side
        - its quite possible / likely that there are more
            TODO: should setup try/catch error handlers to log and analyze
            
### demo task
    - elements to extract (target)
        search aricles (query params: '?s=xxx+yyy')
            ref: https://news.mongabay.com/?s=illegal+logging

        single article scrape
            ref: https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/
    
    - elements to extract, per article (gunther example)
        export: source (organisation/ publisher), date, heading, body text, image, and ideally some information from the body text, i.e. if a certain country or company has been mentionend in the article

### demo log...
    062023_1212: '480p_gun_mbay_demo_062023_1155.mov' & 'TEST_GUN_OUTPUT.csv' delivered via disc
        hello, below you will find your scraping demo for ```news.mongabay.com -> 4 misc articles returned from 'illegal logging' search

        1) .mov file: screen recording demo of the bot running and displaying the scraped data

        2) .csv file: output containing this demo's scraped data``` ... please have a look and provide any feed back or questions when you get a chance... ```Demo notes:
          - this demo represents about 75% of the scraping code base completed for a single site
          - organization & cleanup is still needed, as well as design integrations for timing in staying under the radar 
          - you will notice the image urls are effectively scraped, which makes it easy to save those images to an s3 bucket (if desired)
          - the demo video is in 480p (easier to transfer across discord)... if its too blurry, i can send you the original HD version via email or something like that```
          
### **DESIGN**
    06.20.23 -> latest extracted key/vals (ref: 04_test_gun.py)
        # page_url (str)
        # dt_pub (str)
        # auth_name (str)
        # auth_url (str)
        # header (str)
        # img_header_url (str)
        # img_header_auth (str)
        # body (str)
        # lst_art_imgs (lst)
        # lst_art_img_auths (lst)

        :- example prints of scraped elements
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
        
    analysis
        ref: https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/
        extract -> unique in '04_test_gun_html_1.py'
            source (organisation/ publisher) -> '© 2023 Copyright Conservation news': news.mongabay.com
            author -> <div class="single-article-meta"> by
            dt_published -> <div class="single-article-meta"> by
            heading -> <h1>
            body text -> <article id= ...>
            image header -> <div class="col-lg-12" style="background: ...>
            article images -> <figure id= ...><img decoding= ...>
            image author -> 'Banner image:'
            body query (i.e. search article for country or company name) -> ?
             
    call stack:
        > https://news.mongabay.com/?s=illegal+logging
        > https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/

### Analyzed call stack      
    

### Analyzed call stack (gun):
    
