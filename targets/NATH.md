# TARGETS (NATH)

## nath -> theknot.com
### account log
    - https://www.theknot.com
        (no account creation required, unless creating posts/comments)
        
### goals
    - nathanreimchevu (disc)
        "Looking for a freelancer who can scrape theknot.com for vendors and their phone numbers. Reach out to me via DM with your email and phone number so we can book a call, ..."

### known bugs
    - nil
            
### demo task
    - initial analysis (target)
        call stack (start):
         -> https://www.theknot.com/
            click vendors at top: 
             -> https://www.theknot.com/marketplace
                search by vendor name (auto-complete when typing)
                 -> https://www.theknot.com/marketplace/i-thee-wedd-clarksville-tn-2024860
                    ^ SCRAPE vendor page (name, city/state, phone, about, vendor_page_url)
                search by category & city/state:
                 -> https://www.theknot.com/marketplace/wedding-reception-venues-port-saint-lucie-fl?sort=featured
                    select vendor (^ provides a list of vendors)  
                     -> https://www.theknot.com/marketplace/the-addison-boca-raton-fl-612010
                        ^ SCRAPE vendor page (name, city/state, phone, about, vendor_page_url)
                    
    - elements to extract (target)             
        name, city/state, phone, about
        
    - elements to extract, per vendor (nath example)
        "scrape theknot.com for vendors and their phone numbers”

### demo log...
    - nil
          
### **DESIGN**         
    call stack:
        > https://www.theknot.com/
        > https://www.theknot.com/marketplace
            > https://www.theknot.com/marketplace/i-thee-wedd-clarksville-tn-2024860
            > https://www.theknot.com/marketplace/wedding-reception-venues-port-saint-lucie-fl?sort=featured
                > https://www.theknot.com/marketplace/the-addison-boca-raton-fl-612010

### Analyzed call stack      
    

### Analyzed call stack (nath):
    

