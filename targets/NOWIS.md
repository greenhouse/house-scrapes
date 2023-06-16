# TARGETS (NOWIS)

## nowis -> coursesu.com
### account log
    - no account creation required

### **NOTES**
    - TODO: create updated video demo
        DONE - source code update 
            DONE - scrape data: ingredients, valeurs_nutritionnelles
            DONE - scrape data: collected_at, url
            DONE - print scraped: collected_at, images, url, ingredients, valeurs_nutritionnelles 
        create new video demo and send to NOWIS
         
    - scrape requirements
        ref: nowis discord
            "ean,ingredients,images,marque,nom,nutriscore,url,valeurs_nutritionnelles,collected_at"
        html source analysis
            ref: 
            unknown:
                "ean,,,marque,nom,,,,"

            can pull easily:
                collected_at (date scraped?)
                images
                url
                ingredients
                valeurs_nutritionnelles

            problems pulling:
                nutriscore - not all products on the site have this
                nutriscore - the products that do indeed have this, are in image form

### Analyzed call stack      
    

### Analyzed call stack (nowis):
    



