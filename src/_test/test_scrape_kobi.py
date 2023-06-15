

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
js_file_path = '/Users/greenhouse/devscrape/git/_scrapes/test_scrape_kobi.js'
js_file_path_urls = '/Users/greenhouse/devscrape/git/_scrapes/test_scrape_kobi_urls.js'
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



'''
    here:
        https://www.vfsglobal.com/en/individuals/index.html , -> if for example we select applying from the UK to Italy example to:
        https://visa.vfsglobal.com/gbr/en/ita , then to here:
        https://visa.vfsglobal.com/gbr/en/ita/book-an-appointment and then here:
        https://visa.vfsglobal.com/gbr/en/ita/login
        
        1) GET https://lift-api.vfsglobal.com/master/visacategory/ita/gbr/ILON/en-US
        response json
        [
            {
                "id":3274,"parentId":0,"masterId":0,
                "name":"Italy UK VisaCategory",
                "missionCode":"ita",
                "centerCode":"ILON","code":"UKITVED",
                "culturecode":"en-US","iswaitlist":false,"isTMIEnabled":false,"IsOTPEnable":false,"isVLNNumberEnable":false,"vlnNumberRegex":null,"vlnNumberLabelFormat":null,"enableReferenceNumber":false,"isApplicantDocumentUploadEnabled":false,"isReferenceNumberWithPassportEnabled":false,"IsMaltaExtServiceConsentsEnabled":false,"isApplicantOTPEnabled":false,"isMIGRISNumberEnabled":false,"error":null
            },
            {
                "id":4826,"parentId":0,"masterId":0,
                "name":"Long Stay Catogery",
                "missionCode":"ita",
                "centerCode":"ILON","code":"UKITLSC",
                "culturecode":"en-US","iswaitlist":false,"isTMIEnabled":false,"IsOTPEnable":false,"isVLNNumberEnable":false,"vlnNumberRegex":null,"vlnNumberLabelFormat":null,"enableReferenceNumber":false,"isApplicantDocumentUploadEnabled":false,"isReferenceNumberWithPassportEnabled":false,"IsMaltaExtServiceConsentsEnabled":false,"isApplicantOTPEnabled":false,"isMIGRISNumberEnabled":false,"error":null
            }
        ]
        
        - manually created accnts (house):
            https://visa.vfsglobal.com/gbr/en/dnk
            https://visa.vfsglobal.com/afg/en/aut
            https://visa.vfsglobal.com/vnm/en/bel
        - manually created accnts (temp37):
            https://visa.vfsglobal.com/gbr/en/ita
            https://visa.vfsglobal.com/xkx/en/nor
        - manually created accnts (myst37.001)
            https://visa.vfsglobal.com/vnm/en/bel
            
        *NOTES*
            - current model / plan _ (061423.2313)
                - automate registering email logins for each C in C2M combos (/registration script)
                    - required: need /registration first working in easyHTTP or python
                - manually retrieve tokens for each C in C2M combos (/login manual captcha required)
                - automate checking appointments with each C token in C2M combo (/CheckIsSlotAvailable script)
                
            - registeration requires clicking emailed link: 'ActivateAccount'
                - required: email registration per C in C2M combos
                    - single email can be used for multiple registrations
                    - phone num input should be unique across all registrations
                - TODO: get '/registration' working in easyHTTP or python
                    then we can automate (registering) generating logins for all C in C2M combos

            - 'login' response (among many others in screenshots)
                <div class="errorMessage c-brand-error"> Mandatory field cannot be left blank </div>
            - no single email login for vfsglobal.com
                - each country-to-mission combo requires an email registration
                - emails may indeed be registered w/ more than one country-to-mission combo
                - passwords are not shared amongst email logins for different country-to-mission combos
                - country-to-mission combo ex: /afg/en/aut, /vnm/en/bel, /gbr/end/dnk
                - each country-to-mission combo has its own vacCode & visaCategoryCode sets used in 'CheckIsSlotAvailable'
                - email login/pw is indeed bound to just 'country' in the C2M combo (some combos can use the same token after)
                    - created accnts (house):
                        https://visa.vfsglobal.com/gbr/en/dnk
                    - logins success (house): -> note: nzl and est can ues the same token
                        https://visa.vfsglobal.com/gbr/en/dnk
                        https://visa.vfsglobal.com/gbr/en/nzl
                        https://visa.vfsglobal.com/gbr/en/est
                        https://visa.vfsglobal.com/gbr/en/prt
                            
        0) POST https://lift-api.vfsglobal.com/user/registration
            Chrome browser inspect 'Name': 'registration'
                request headers
                    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
                    Content-Type: application/json;charset=UTF-8
                    request payload
                    {
                        "emailid":"housesellout@gmail.com",
                        "password":"Password123!",
                        "confirmPassword":"Password123!",
                        "instructionAgreed":true,
                        "missioncode":"bel",
                        "countrycode":"vnm",
                        "languageCode":"en",
                        "dialcode":"1",
                        "contact":"7327660010",
                        "cultureCode":"en-US"
                    }
                
                response headers
                    Content-Type: application/json
                    response json
                    {
                        "code": "200",
                        "message": "Registration done successfully. To proceed with the appointment system, kindly activate your account by clicking on the activation link received in your email account used while registration.",
                        "error": null
                    }
                
        
        
        1) POST https://visa.vfsglobal.com/afg/en/aut/login
            Chrome browser inspect 'Name': 'login'
                request headers
                    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
                    Content-Type: application/x-www-form-urlencoded
                    request payload
                        username=housesellout@gmail.com
                        &password=Password123!
                        &missioncode=aut
                        &countrycode=afg
                        &captcha_version=v2
                        &captcha_api_key=03AL8...Zcpg
                
                response headers
                    Content-Type: application/json
                    response json
                    {
                        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6IjljUEU2S1FzREZwbzJoSnFaUEtObDFVSlJBdVdIdmJCRG92TU1MSjZkR1E9IiwiZW1haWwiOiJSVUZjMXFmUEZ4bmNIN09xY1BRTHMxRGE4ay9QcWVESUF5bUlsSW9ZcTBBSTJZa3AvSDBBQ3lvWWV0QU13SmF5IiwibmJmIjoxNjg2NzcyNDYwLCJleHAiOjE2ODY3Nzg0NjAsImlhdCI6MTY4Njc3MjQ2MH0.l6AOnN7AHZtZyAKXYIXuXJUwS3qaHuNSB6OpnbB1X18",
                        "isAuthenticated": true,
                        "nearestVACCountryCode": null,
                        "FailedAttemptCount": 0,
                        "isAppointmentBooked": false,
                        "isLastTransactionPending": false,
                        "isAppointmentExpired": false,
                        "isLimitedDashboard": false,
                        "isROCompleted": false,
                        "isSOCompleted": false,
                        "roleName": "Individual",
                        "isUkraineScheme": false,
                        "isUkraineSchemeDocumentUpload": false,
                        "loginUser": "housesellout@gmail.com",
                        "dialCode": "1",
                        "contactNumber": "7327660120",
                        "remainingCount": 0,
                        "accountLockHours": 2,
                        "enableOTPAuthentication": false,
                        "error": null
                    }

        2) POST https://lift-api.vfsglobal.com/appointment/CheckIsSlotAvailable
            Chrome browser inspect 'Name': 'CheckIsSlotAvailable'
                request headers (from chrome browser inspect, after 'login')
                    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
                    Content-Type: application/json;charset=UTF-8
                    Authorize: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6ImV2TXh0S0Vhb05ZVzU4TWtGZWo3dEE9PSIsImVtYWlsIjoiUlVGYzFxZlBGeG5jSDdPcWNQUUxzMURhOGsvUHFlRElBeW1JbElvWXEwQUkyWWtwL0gwQUN5b1lldEFNd0pheSIsIm5iZiI6MTY4Njc2NzUxMCwiZXhwIjoxNjg2NzczNTEwLCJpYXQiOjE2ODY3Njc1MTB9.g02GK9LQRp_oV0CfRsS_hfUowdtw2DjnTylsT6YVTRo
                    
                    request payload (ex 1)
                    {
                      "countryCode": "gbr",
                      "missionCode": "ita",
                      "vacCode": "ILON", // ITLYEDN, ILON, IMAN
                      "visaCategoryCode": "TBE", // LSNBN, TBE, NVD
                      "roleName": "Individual",
                      "loginUser": "temp37373737@gmail.com"
                    }
                
                    request payload (ex 2)
                    {
                        "countryCode":"gbr",
                        "missionCode":"dnk",
                        "vacCode":"EDI",
                        "visaCategoryCode":"Den",
                        "roleName":"Individual",
                        "loginUser":"housesellout@gmail.com"
                    }
                    
                    request payload (ex 3)
                    {
                        "countryCode":"afg",
                        "missionCode":"aut",
                        "vacCode":"ILON",
                        "visaCategoryCode":"TBE",
                        "roleName":"Individual",
                        "loginUser":"housesellout@gmail.com"
                    }
                    {
                        "countryCode":"afg",
                        "missionCode":"aut",
                        "vacCode":"AUT-AFG",
                        "visaCategoryCode":"OF",
                        "roleName":"Individual",
                        "loginUser":"housesellout@gmail.com"
                    }
                
                response headers (from chrome browser inspect, after login)
                    Content-Type: application/json
                    response json (ex 1)
                    {
                        "earliestDate":null,
                        "error":
                            {
                                "code":1035,
                                "description":"No slots available"
                            }
                    }
                    
                    response json (ex 2)... occurs on 'visaCategoryCode' error
                    {
                        "earliestDate":null,
                        "error":
                            {
                                "code":1008,
                                "description":"Visacategory does not exist"
                            }
                    }
                    
                    response json (ex 3)... occurs on 'vacCode' error
                    {
                        "earliestDate":null,
                        "error":
                        {
                            "code":1007,
                            "description":"Center does not exists."
                        }
                    }
                    
                    response json (ex 4)
                    {
                        "earliestDate":"06/27/2023 00:00:00",
                        "error":null
                    }

        3) POST https://lift-api.vfsglobal.com/appointment/applicants
            Tor browser inspect 'Name': 'applicants'
                request headers (from browser inspect, after 'CheckIsSlotAvailable')
                    User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0
                    Content-Type: application/json;charset=UTF-8
                    Authorize: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6ImV2TXh0S0Vhb05ZVzU4TWtGZWo3dEE9PSIsImVtYWlsIjoiUlVGYzFxZlBGeG5jSDdPcWNQUUxzMURhOGsvUHFlRElBeW1JbElvWXEwQUkyWWtwL0gwQUN5b1lldEFNd0pheSIsIm5iZiI6MTY4Njc2NzUxMCwiZXhwIjoxNjg2NzczNTEwLCJpYXQiOjE2ODY3Njc1MTB9.g02GK9LQRp_oV0CfRsS_hfUowdtw2DjnTylsT6YVTRo
                    
                    request payload (ex 1)
                    {
                        "countryCode": "vnm",
                        "missionCode": "bel",
                        "centerCode": "BEHO",
                        "loginUser": "housesellout@gmail.com",
                        "visaCategoryCode": "08",
                        "isEdit": false,
                        "feeEntryTypeCode": null,
                        "feeExemptionTypeCode": null,
                        "feeExemptionDetailsCode": null,
                        "applicantList": [
                            {
                                "urn": "",
                                "arn": "",
                                "loginUser": "housesellout@gmail.com",
                                "firstName": "HELLO",
                                "middleName": "",
                                "lastName": "WORLD",
                                "salutation": "",
                                "gender": 1,
                                "nationalId": null,
                                "VisaToken": null,
                                "contactNumber": "7327660010",
                                "dialCode": "1",
                                "passportNumber": "63",
                                "confirmPassportNumber": "",
                                "passportExpirtyDate": "25/06/2038",
                                "dateOfBirth": "12/06/1971",
                                "emailId": "housesellout@gmail.com",
                                "nationalityCode": "CHN",
                                "state": null,
                                "city": null,
                                "isEndorsedChild": false,
                                "applicantType": 0,
                                "addressline1": null,
                                "addressline2": null,
                                "pincode": null,
                                "referenceNumber": null,
                                "vlnNumber": null,
                                "applicantGroupId": 0,
                                "parentPassportNumber": "",
                                "parentPassportExpiry": "",
                                "dateOfDeparture": null,
                                "gwfNumber": "",
                                "entryType": "",
                                "eoiVisaType": "",
                                "passportType": "",
                                "ipAddress": "199.249.230.87"
                            }
                        ],
                        "languageCode": "en-US",
                        "isWaitlist": false
                    }
                    
                response headers (unknown for 200OK)
                    content-type: application/json -> (for 403Forbidden)
                    
                    
'''
