
#============================================#
# use existing browser instance
#============================================#
#import asyncio
#from pyppeteer import connect
#
#async def main():
#    # Connect to an existing browser instance
#    browser = await connect(browserWSEndpoint='ws://127.0.0.1:9222/devtools/browser/<BROWSER_ID>')
#
#    # Create a new page
#    page = await browser.newPage()
#
#    # Navigate to example.com
#    await page.goto('https://www.example.com')
#
#    # Click the "I'm Feeling Lucky" button
#    selector = 'input[value="I\'m Feeling Lucky"]'  # Assuming the button is an input element
#    await page.waitForSelector(selector)  # Wait for the button to be present
#    await page.click(selector)
#
#    # Wait for some time to see the effect (optional)
#    await asyncio.sleep(2)
#
#    # Close the page
#    await page.close()
#
#    # Close the browser (optional if you want to keep the browser running)
#    await browser.close()
#
## Run the main function
#asyncio.run(main())
#
#exit(0)


#============================================#
# launch new browser instance
#============================================#
import asyncio
from pyppeteer import launch
from pyppeteer import connect
import time

PATH_CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PATH_TOR = '/Applications/Tor Browser.app/Contents/MacOS/firefox'
PATH_FIRE = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
PATH_SAFARI = '/Applications/Safari.app/Contents/MacOS/Safari'
PATH_CHROMIUM = '/Applications/Chromium.app/Contents/MacOS/Chromium'

async def main():
    # Launch the browser
#    browser = await launch(executablePath=PATH_CHROMIUM, headless=False)
#    browser = await launch(executablePath=PATH_CHROME, headless=False)
    #browser = await launch(headless=False)
    
#    browser = await connect(browserWSEndpoint='ws://127.0.0.1:9222/devtools/browser/<BROWSER_ID>')
    browser = await connect(browserWSEndpoint='ws://127.0.0.1:9222/devtools/browser/3146')
    
    
    
    # Create a new page
    page = await browser.newPage()
    
    # Navigate to example.com
    await page.goto('https://www.google.com')
    
    print('sleep(5)...')
    await asyncio.sleep(5)
#    time.sleep(5)
    # Click the "I'm Feeling Lucky" button
    print('proceed with click')
    selector = 'input[value="I\'m Feeling Lucky"]'  # Assuming the button is an input element
    await page.waitForSelector(selector)  # Wait for the button to be present
    await page.click(selector)
    
    # Wait for some time to see the effect (optional)
    print('sleep(2)...')
    await asyncio.sleep(2)
    
    # Close the browser
    print('browser.close()')
#    await browser.close()

# Run the main function
asyncio.run(main())

