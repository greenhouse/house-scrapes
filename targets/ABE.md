# TARGETS (ABE _ hackerabe)

## abe -> target.com
### account log
    - https://target.com
        (no account creation required)
        
### goals
    - abe (disc)
        "Hey, I want to scrap all the products/items of target.com"
        "just one single dump of the data"
        "I think it’s gonna be around 250k - 350k products"
        "Im looking to get something like this (per product):"

### demo task
    - elements to extract (target)
        search products (query params: '?searchTerm=xxx')
            ref: https://www.target.com/s?searchTerm=gameboy+advance
            ref: https://www.target.com/s?searchTerm=airpods+pro
        single product scan
            ref: https://www.target.com/p/world-poker-tour-for-gameboy-advance/-/A-86125353#lnk=sametab
            reF: https://www.target.com/p/apple-airpods-pro-2nd-generation/-/A-85978612#lnk=sametab
        product images
            max 4 main image buttons on left side -> <button><div><div><div><picture><img src='...'>
             there is also an option to select more images, but i can't find the imgs in the code
        "About this item"
            "At a glance:" -> ('Description' covers this)
                True Wireless
                Noise Canceling
                Built-In Microphone
                Water Resistant
            "Highlights:"
                - Up to 2x more Active Noise Cancellation than the previous generation AirPods Pro, so you’ll hear dramatically less noise during your commute and when you need to focus.¹
                - Apple-designed H2 chip, the new force behind AirPods Pro, pushes advanced audio performance even further. From smarter noise cancellation to superior three-dimensional sound and battery life, it improves on the best features of AirPods Pro in a big way.
                - Low distortion, custom-built driver and amplifier delivers crisp, clear high notes and deep, rich bass in stunning definition. Every sound is more vivid than ever.
                - ...
            "Specifications"
                Weight: 1.34 Ounces
                Water Resistance: Sweat-Resistant, Water-Resistant
                Ear Cushion Material: ABS (Acrylonitrile Butadiene Styrene)
                Estimated Charge Time: 6 Hours
                Connection Types: Apple Lightning Connector
                Wireless Technology: True Wireless
                Package Quantity: 1
                Noise Canceling: Noise Canceling
                Microphone: Built-In Microphone
                Maximum Battery Charge Life: 30 Hours
                Battery: 1 Non-Universal Lithium Ion, Required, Included
                Warranty: 1 Year Limited Warranty. To obtain ... Target Guest Services at 1-800-591-3869
                Street Date: September 22, 2022
                TCIN: 85978612
                UPC: 194253397168
                Item Number (DPCI): 057-10-1605
                Origin: Imported
            "Description"
                AirPods ... listening time.³
                Legal
                Technical specifications
                    Go to apple.com/airpods-pro/specs/ for a complete set.
                True Wireless
                    Ear buds that are designed without a cord or wire and is connected via Bluetooth
                Noise Canceling
                    Reduces unwanted sounds using active noise control.
                Built-In Microphone
                    Comes with a microphone that is used for recording
                Water Resistant
                    Product is able to resist the penetration of water to some degree.
            "Shipping & Returns"
                "Shipping details"
                    ...
                "Return details"
                    ...

    - elements to extract, per product (abe example)
        {
            "upc": "062338988641", -> # found
            "ean": "0062338988641",
            "elid": "143999815329",
            "gtin": "00062338988641",
            "sku": "",
            "internal_product_numbers": {
                "dpci": "",
                "tcin": "",
                "asin": "",
                "part_number": ""
            },
            "product_name": "Air Wick Pure Freshmatic Automatic Spray Refill, 5.89 Ounce, Sparkling Citrus, Air Freshener",
            "size": "5.89 Ounce",
            "model": "",
            "brand": "Air Wick",
            "owner": "Reckitt",
            "product_url": "https://www.walmart.com/ip/Air ... Refill-Pure-Sparkling-Citrus-6-17-oz-Pack-of-2/201676260",
            "country": "us",
            "category": "Home & Garden > Decor > Home Fragrances > Air Fresheners",
            "description": "Pure Sparkling Citrus Fragrance with ... room: living room, bathroom, hallways, kitchens, den and office",
            "ingredients": "",
            "lowest_recorded_price": 2.4,
            "highest_recorded_price": 59.75,
            "date_first_seen": "20230328",
            "date_last_seen": "20230328"
        }

### **DESIGN**
    call stack:
        > https://www.target.com/s?searchTerm=airpods+pro
        > https://www.target.com/p/apple-airpods-pro-2nd-generation/-/A-85978612#lnk=sametab
    
### Analyzed call stack      
    

### Analyzed call stack (abe):
    
