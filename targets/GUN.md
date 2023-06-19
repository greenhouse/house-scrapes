# TARGETS (ABE _ hackerabe)

## gun -> news.mongabay.com
### account log
    - https://news.mongabay.com
        (no account creation required)
        
### goals
    - gunther (disc)
        "Hi there. These would be a list of websites that I would like to crawl for news articles for specific keywords (e.g. illegal logging). From those articles, I want to export: source (organisation/ publisher), date, heading, body text, image, and ideally some information from the body text, i.e. if a certain country or company has been mentionend in the article"
        "that's correct. I want to search for specific keywords/ news topics"

### demo task
    - elements to extract (target)
        search aricles (query params: '?s=xxx+yyy')
            ref: https://news.mongabay.com/?s=illegal+logging

        single article scrape
            ref: https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/
    
    - elements to extract, per article (gunther example)
        export: source (organisation/ publisher), date, heading, body text, image, and ideally some information from the body text, i.e. if a certain country or company has been mentionend in the article
        

### **DESIGN**
    analysis
        ref: https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/
        extract: (ref: 04_test_gun_html_1.py)
            source (organisation/ publisher) -> '© 2023 Copyright Conservation news': news.mongabay.com
            author  -> line #251 (<div class="single-article-meta"> by)
            dt_published -> line #251 (<div class="single-article-meta"> by)
            heading -> line #249 (<h1>)
            body text -> line #279 (<article id= ...>)
            image header -> line #274 (<div class="col-lg-12" style="background: ...>)
            article images -> line #289 (<figure id= ...><img decoding= ...>)
            image author -> line #299 ('Banner image:')
            body query (i.e. search article for country or company name) -> 
    call stack:
        > https://news.mongabay.com/?s=illegal+logging
        > https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/

### Analyzed call stack      
    

### Analyzed call stack (gun):
    
