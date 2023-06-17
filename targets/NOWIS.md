# TARGETS (NOWIS)

## nowis -> coursesu.com
### account log
    - https://www.coursesu.com
        (no account creation required)
        
### **DEISNG**
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

    SCALABLE EXTRACTION (post-demo)
        1) it appears that launching browsers through code, leads to a 'banned' message
            GET https://www.coursesu.com/c/charcuterie-traiteur/charcuterie/jambon-blanc?page=2
        2) using regular GUI browser works just fine (not launching through code)
            doesn't appear to be the IP thats blocked
        3) maybe try new VPN on AWS (doesn't make much sense considering #2)
        4) maybe somehow try to start running automation 'after' manual GUI browser is already launched
            #=========================================#
            # enable Chrome DevTools Protocol w/ browser (mac osx)
            #=========================================#
            $ /Applications/Chromium.app/Contents/MacOS/Chromium --remote-debugging-port=9222
            $ /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --remote-debugging-port=9222
            $ /Applications/Tor Browser.app/Contents/MacOS/firefox --remote-debugging-port=9222
            $ /Applications/Firefox.app/Contents/MacOS/firefox-bin --remote-debugging-port=9222
            $ /Applications/Safari.app/Contents/MacOS/Safari --remote-debugging-port=9222
            $ /Applications/Chromium.app/Contents/MacOS/Chromium --remote-debugging-port=9222
            $ /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

### Analyzed call stack      
    

### Analyzed call stack (nowis):
    



