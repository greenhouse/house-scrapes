

'''
    house_061323:
        create regex to filter uri params for 'https://visa.vfsglobal.com/x1/x2/x3'
        - there are 1152 unique urls... len(unique_matches): 1152
'''
import json
import os
import re

def print_js_file(file_path):
    print('enter _ print_js_file')
    with open(file_path, 'r') as file:
        print('enter with open')
        lines = file.readlines()
        print('lines:\n', *lines, sep='')
        print(f'len(lines): {len(lines)}\n\n')
        print('exit _ print_js_file')
        
def filter_js_file_regex(file_path):
    print('enter _ filter_js_file_regex')
    
    #url: "https://visa.vfsglobal.com"
    pattern = r'^(?!.*_url.*)(.*url: "https://visa.vfsglobal.com/.*|.*"url": "https://visa.vfsglobal.com/.*)'
    
    with open(file_path, 'r') as file:
        print('enter with open')
        lines = file.readlines()
        js_string = ''.join(lines)
        matches = re.findall(pattern, js_string, re.MULTILINE)
        unique_matches = list(set(matches))

        # format to usable list of strings (links)
        unique_matches = [re.sub(r'url:', '', line) for line in unique_matches]
        unique_matches = [re.sub(r'"url":', '', line) for line in unique_matches]
        unique_matches = [re.sub(r'"', '', line) for line in unique_matches]
        unique_matches = [re.sub(r',', '', line) for line in unique_matches]
        unique_matches = [line[:-1] if line[-1] == '/' else line for line in unique_matches]
        unique_matches = [re.sub(r' ', '', line) for line in unique_matches]
        
        # handle misc duplicates & invalids
        unique_matches = [line for line in unique_matches if not line.endswith('/contact-us')]
        unique_matches = [line for line in unique_matches if not line.endswith('/attend-centre')]
        unique_matches = [line for line in unique_matches if not line.endswith('/en')]
        
        # print log
        print('unique_matches: ', *unique_matches, sep='\n')
        print(f'len(unique_matches): {len(unique_matches)}\n\n')
        
        # log / parse countryCode & missionCode
        for i,v in enumerate(unique_matches):
            slice_1 = v.split('https://visa.vfsglobal.com/')[1]
            if len(slice_1.split('/')) < 3: continue
            ret_0 = slice_1.split('/')[0] # countryCode
            ret_1 = slice_1.split('/')[1] # 'en'
            ret_2 = slice_1.split('/')[2] # missionCode
            print(f"{i}:", ret_0, ret_1, ret_2)
            
        filtered_js_code = '\n'.join(unique_matches)
        #print(f'filtered_js_code: {filtered_js_code}')
        print('exit _ filter_js_file_regex')
        return unique_matches # filtered_js_code

def filter_js_string_regex(js_string):
    print('enter _ filter_js_string_regex')
    pattern = r'^(?!.*_url.*)(.*url: "https://visa.vfsglobal.com/.*)'
    matches = re.findall(pattern, js_string, re.MULTILINE)
    unique_matches = list(set(matches))
    filtered_js_code = '\n'.join(unique_matches)
    return filtered_js_code

# Example usage
js_file_path = './test_scrape_kobi.js'
js_file_path_urls = './test_scrape_kobi_urls.js'
print_js_file(js_file_path_urls)
#lst_urls = filter_js_file_regex(js_file_path)

#filtered_js_code = filter_js_string_regex(str_blob)
#filtered_js_code = filter_js_string(str_blob)
#filtered_js_code = filter_js_file(js_file_path)
#print(filtered_js_code)
print('*** exiting ***')
exit(0)




 
import requests
import json
import time

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

