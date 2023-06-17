# TARGETS (KUNA _ kunalghiya)

## kuna -> yourstory.com
### account log
    - https://yourstory.com
        (no account creation required)
        
### goals
    - kuna (disc)
        "Okay so our main thing what i want to do is we feed chatGPT all the articles related to this one company and then make it rewrite a new article for us.."

### demo task
    - elements to extract
        company name, 
        company founders, 
        total funding raised, 
        names of investors, 
        where they are based out of.. 
    - from a few different articles in...
        https://yourstory.com/search?page=1&category=Funding
        NOTE: '?page=0' returns empty lst of results (no error msg)

### **DESIGN**
    GENERAL EXTRACTION
        1) loop through 50 pages of search results with: https://yourstory.com/search?page=1&category=Funding
            each page has 20 article URIs, embedded within <div><div><li><a href='...'> tags
                ex: href='/2023/06/weekly-funding-roundup-june-12-16-vc-investments-rise-lenskart'
        2) scrape html from article links and search for elementst to extract
            ex: 'https://yourstory.com/2023/06/weekly-funding-roundup-june-12-16-vc-investments-rise-lenskart'
            
    DEMO EXTRACTION (screen-record)
        1) just use '?page=1'
        2) just scrape 4 article htmls & print elements 
        3) wait 2 sec before each html
            
    SCALABLE EXTRACTION (post-demo)
        1) need to scrape html from ~1000 articles (urls)
        2) don't want to set off alarms
        3) maybe get html content first, and then search for elements later
        
### Analyzed call stack      
    

### Analyzed call stack (kuna):
    



