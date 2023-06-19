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
    call stack:
        > https://news.mongabay.com/?s=illegal+logging
        > https://news.mongabay.com/2023/03/indonesian-campaigns-getting-money-from-illegal-logging-mining-watchdog-says/

### Analyzed call stack      
    

### Analyzed call stack (gun):
    
