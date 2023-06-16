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

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
# NOTE_061623:
#   manually login & get authorize tokens for each created acct (x6)

url = 'https://lift-api.vfsglobal.com/appointment/CheckIsSlotAvailable'
headers = {
    'Content-Type': 'application/json',
    'Authorize': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6InYxL282QjN6YU1Sd1JsMzY5S2hzNG9qY0hrN1RrSjRwVFNNL1FKbmZhSFE9IiwiZW1haWwiOiJqemNrdStPcWQyeFg5YWlDWTZDT3VlMzlMOVpNdzY2Yy9kZVRXdUJqbjBSeDZqdWZ5alkzMSt5Nno4ZWZzcGJKIiwibmJmIjoxNjg2NjgyMDY1LCJleHAiOjE2ODY2ODgwNjUsImlhdCI6MTY4NjY4MjA2NX0.5VIBzsbjRTPJqsSPaYHjo5kXbsJQvTn2iafJjUvsFkc'
}

payload = {
    'countryCode': 'gbr',
    'missionCode': 'ita',
    'vacCode': 'ILON',  # ITLYEDN, ILON, IMAN
    'visaCategoryCode': 'TBE',  # LSNBN, TBE, NVD
    'roleName': 'Individual',
    'loginUser': 'temp37373737@gmail.com'
}

lst_vacCode = ['ITLYEDN', 'ILON', 'IMAN']
lst_catCode = ['LSNBN', 'TBE', 'NVD']

sleep_sec = 5
for i in lst_vacCode:
    vac_code = lst_vacCode[i]
    payload['vacCode'] = vac_code
    for j in lst_catCode:
        cat_code = lst_catCode[j]
        payload['visaCategoryCode'] = cat_code
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        print(response.status_code)
        print(response.json())
        
        print(f'\n\n *** sleep({sleep_sec}) *** \n\n')
        time.sleep(sleep_sec)


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

