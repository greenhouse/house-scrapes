#!/usr/bin/env python
__filename = 'kobi_vfsglobal_scrape.py'
__fname = 'kobi_vfsglobal_scrape'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import requests
import json
import time
from datetime import datetime
#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
'''    
    NOTE_061623: manually login & get authorize tokens for each created acct (x6)
        - manually created accnts (house):
            https://visa.vfsglobal.com/gbr/en/dnk
            https://visa.vfsglobal.com/afg/en/aut
            https://visa.vfsglobal.com/vnm/en/bel
        - manually created accnts (temp37):
            https://visa.vfsglobal.com/gbr/en/ita
            https://visa.vfsglobal.com/xkx/en/nor
        - manually created accnts (myst37.001)
            https://visa.vfsglobal.com/vnm/en/bel
'''
#==============================================#
# C2M: https://visa.vfsglobal.com/gbr/en/ita (temp37)
#==============================================#
'''
:Authority:
lift-api.vfsglobal.com
:Method:
OPTIONS
:Path:
/appointment/CheckIsSlotAvailable
:Scheme:
https
Accept:
*/*
Accept-Encoding:
gzip, deflate, br
Accept-Language:
en-US,en;q=0.9
Access-Control-Request-Headers:
authorize,content-type,route
Access-Control-Request-Method:
POST
Origin:
https://visa.vfsglobal.com
Referer:
https://visa.vfsglobal.com/
Sec-Fetch-Dest:
empty
Sec-Fetch-Mode:
cors
Sec-Fetch-Site:
same-site
Sec-Gpc:
1
User-Agent:
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
'''



#blob = '''
'''
:Authority:
lift-api.vfsglobal.com
:Method:
POST
:Path:
/appointment/CheckIsSlotAvailable
:Scheme:
https
Accept:
application/json, text/plain, */*
Accept-Encoding:
gzip, deflate, br
Accept-Language:
en-US,en;q=0.9
Authorize:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6InYxL282QjN6YU1Sd1JsMzY5S2hzNG9qY0hrN1RrSjRwVFNNL1FKbmZhSFE9IiwiZW1haWwiOiJqemNrdStPcWQyeFg5YWlDWTZDT3VlMzlMOVpNdzY2Yy9kZVRXdUJqbjBSeDZqdWZ5alkzMSt5Nno4ZWZzcGJKIiwibmJmIjoxNjg2OTQwMjA5LCJleHAiOjE2ODY5NDYyMDksImlhdCI6MTY4Njk0MDIwOX0.mcFKChdP9E3dP6dQl4DY4T9pmxae9PhoRfB-UfS_7nQ
Content-Length:
147
Content-Type:
application/json;charset=UTF-8
Origin:
https://visa.vfsglobal.com
Referer:
https://visa.vfsglobal.com/
Route:
gbr/en/ita
Sec-Ch-Ua:
"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
Sec-Ch-Ua-Mobile:
?0
Sec-Ch-Ua-Platform:
"macOS"
Sec-Fetch-Dest:
empty
Sec-Fetch-Mode:
cors
Sec-Fetch-Site:
same-site
Sec-Gpc:
1
User-Agent:
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
'''
#headers = {}
#lines = blob.strip().split('\n')
#
#for i in range(0, len(lines), 2):
#    key = lines[i].strip(':')
#    value = lines[i+1].strip()
#    headers[key] = value
#
#print(headers)
#exit(0)

url = 'https://lift-api.vfsglobal.com/appointment/CheckIsSlotAvailable'
#headers = {
#    'Content-Type': 'application/json;charset=UTF-8',
#    'Authorize': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6InYxL282QjN6YU1Sd1JsMzY5S2hzNG9qY0hrN1RrSjRwVFNNL1FKbmZhSFE9IiwiZW1haWwiOiJqemNrdStPcWQyeFg5YWlDWTZDT3VlMzlMOVpNdzY2Yy9kZVRXdUJqbjBSeDZqdWZ5alkzMSt5Nno4ZWZzcGJKIiwibmJmIjoxNjg2OTQwMjA5LCJleHAiOjE2ODY5NDYyMDksImlhdCI6MTY4Njk0MDIwOX0.mcFKChdP9E3dP6dQl4DY4T9pmxae9PhoRfB-UfS_7nQ'
#}

headers = {
    'Authority': 'lift-api.vfsglobal.com',
    'Method': 'POST',
    'Path': '/appointment/CheckIsSlotAvailable',
    'Scheme': 'https',
    'Accept': 'application/json, text/plain, */*',
    #'Accept-Encoding': 'gzip, deflate, br', # causes weird flashing & binary overlay in CLI
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorize': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6InYxL282QjN6YU1Sd1JsMzY5S2hzNG9qY0hrN1RrSjRwVFNNL1FKbmZhSFE9IiwiZW1haWwiOiJqemNrdStPcWQyeFg5YWlDWTZDT3VlMzlMOVpNdzY2Yy9kZVRXdUJqbjBSeDZqdWZ5alkzMSt5Nno4ZWZzcGJKIiwibmJmIjoxNjg2OTU2NDgyLCJleHAiOjE2ODY5NjI0ODIsImlhdCI6MTY4Njk1NjQ4Mn0.yMKzwPjPfrbefvC_CphOOUivm91va8ydyK2KUc7RF_0',
    'Content-Length': '149',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://visa.vfsglobal.com',
    'Referer': 'https://visa.vfsglobal.com/',
    'Route': 'gbr/en/ita',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Gpc': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

o_headers = {
    'Authority': 'lift-api.vfsglobal.com',
    'Method': 'OPTIONS',
    'Path': '/appointment/CheckIsSlotAvailable',
    'Scheme': 'https',
    'Accept': '*/*',
    #'Accept-Encoding': 'gzip, deflate, br', # causes weird flashing & binary overlay in CLI
    'Accept-Language': 'en-US,en;q=0.9',
    'Access-Control-Request-Headers': 'authorize,content-type,route',
    'Access-Control-Request-Method': 'POST',
    'Origin': 'https://visa.vfsglobal.com',
    'Referer': 'https://visa.vfsglobal.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Gpc': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

payload = {
    'countryCode': 'gbr',
    'missionCode': 'ita',
    'vacCode': 'ITLYEDN',  # ITLYEDN, ILON, IMAN
    'visaCategoryCode': 'LSNBN',  # LSNBN, TBE, NVD
    'roleName': 'Individual',
    'loginUser': 'temp37373737@gmail.com'
}

def get_time_now():
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
lst_vacCode = ['ITLYEDN', 'ILON', 'IMAN']
lst_catCode = ['LSNBN', 'TBE', 'NVD']

sleep_sec = 30
for i in lst_vacCode:
#    vac_code = lst_vacCode[i]
    vac_code = i
#    payload['vacCode'] = vac_code
    for j in lst_catCode:
#        cat_code = lst_catCode[j]
        cat_code = j
#        payload['visaCategoryCode'] = cat_code
        print(f'\n\nvac_code: {vac_code}')
        print(f'cat_code: {cat_code}')
        
        print(f'\nexecuting OPTIONS request... - {get_time_now()}')
        response = requests.options(url, headers=o_headers)
        print(f'executing OPTIONS request... DONE - {get_time_now()}')

        print(f'\n*** status_code ***: {response.status_code}')
        print(f'*** response.json ***: {response.json}')
        print(f'*** response.content ***:\n{response.text}') # .content=minified | .text=formated
        
        time.sleep(1)
        #TODO: ... left off here
        '''
            1) can't get native http request to work for:
                POST | OPTIONS https://lift-api.vfsglobal.com/appointment/CheckIsSlotAvailable
            2) keep getting 403 access denied
            3) browser manual GUI works just fine
                doesn't appear to be the IP thats blocked
            4) maybe try new VPN on AWS
                doesn't make much sense considering #3
            5) maybe somehow try to start running automation
                AFTER manual GUI browser is already launched
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
        '''
        
        print(f'\nexecuting POST request... - {get_time_now()}')
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f'executing POST request... DONE - {get_time_now()}')
        
        print(f'\n*** status_code ***: {response.status_code}')
        print(f'*** response.json ***: {response.json}')
        print(f'*** response.content ***:\n{response.text}') # .content=minified | .text=formated

        #print(f'\n\n *** sleep({sleep_sec}) *** \n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(f'\n\n *** sleep({sleep_sec}) *** ... start')
        
        exit(0)
        i = sleep_sec
        while i >= 0:
            print(i, sep='', end='\n')
            time.sleep(1)
            i -= 1
            
#        [time.sleep(1) while i>=0 ]
#        time.sleep(sleep_sec)


#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
#def go_main():
#    run_time_start = get_time_now()
#    print(f'\n\nRUN_TIME_START: {run_time_start}')
#    read_cli_args() # print cli args
#    argCnt = len(sys.argv) # get arg cnt
#
#    # validate args
#    if argCnt > 1:
#        print('*** ERROR *** _ invalid args\n ... exiting\n\n')
#        exit(1)
#
#    # loop through and scrape each url
#    exe_pg_scrape_loop(LST_PG_URLS, WAIT_TIME)
#
#    print(f'\n\nRUN_TIME_START: {run_time_start}')
#    print(f'RUN_TIME_END:   {get_time_now()}')
#
#def read_cli_args():
#    funcname = f'<{__filename}> _ ENTER _ read_cli_args'
#    print(f'\n{funcname}...')
#    argCnt = len(sys.argv)
#    print(' # of args: %i' % argCnt)
#    print(' argv lst: %s' % str(sys.argv))
#    for idx, val in enumerate(sys.argv):
#        print(f' argv[{idx}]: {val}')
#    print(f'DONE _  read_cli_args...')
#
#if __name__ == "__main__":
#    go_main()


