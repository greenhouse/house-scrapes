# TARGETS (KOBI)

## kobi -> vfsglobal.com
### account log
    - manually created accnts (house):
        https://visa.vfsglobal.com/gbr/en/dnk
        https://visa.vfsglobal.com/afg/en/aut
        https://visa.vfsglobal.com/vnm/en/bel
    - manually created accnts (temp37):
        https://visa.vfsglobal.com/gbr/en/ita
        https://visa.vfsglobal.com/xkx/en/nor
    - manually created accnts (myst37.001)
        https://visa.vfsglobal.com/vnm/en/bel

### **NOTES**
    - TODO: create video demo
        - traversing through 'manually created accnts' C2M urls (x6)
            manually login & get authorize tokens for each
        - automate checking all param combos within each C2M url (x6)
            useing '/CheckIsSlotAvailable'
        - print each param combo / C2M result... x(y1+...+y6)
            # success (appt avail) -> {earliestDate, error:null}
                "error":null 
                "earliestDate":"06/27/2023 00:00:00",
            
            # error (no appt avail) -> {earliestDate, error:{code, description}}
                "earliestDate":null,
                "description":"No slots available" # "code":1035,
                "description":"Visacategory does not exist" # "code":1008,
                "description":"Center does not exists." # "code":1007,
                    
    - TODO: get '/registration' working in easyHTTP or python (only manual click currently works)
        then we can automate (registering) generating logins for all (244) C in C2M combos
            ref: https://www.vfsglobal.com/en/individuals/index.html
            search-source-code: 'Online Visa Application'
            
    - current model / plan _ (061423.2313)
        - automate registering email logins for each C in C2M combos (/registration script)
            - required: need /registration first working in easyHTTP or python
        - manually retrieve tokens for each C in C2M combos (/login manual captcha required)
        - automate checking appointments with each C token in C2M combo (/CheckIsSlotAvailable script)
        
    - registeration requires clicking emailed link: 'ActivateAccount'
        - required: email registration per C in C2M combos
            - single email can be used for multiple registrations
            - phone num input should be unique across all registrations

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
                     
### Analyzed call stack      
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

    1) POST https://lift-api.vfsglobal.com/user/login (GUI: https://visa.vfsglobal.com/afg/en/aut/login)
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
                    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6InYxL282QjN6YU1Sd1JsMzY5S2hzNG9qY0hrN1RrSjRwVFNNL1FKbmZhSFE9IiwiZW1haWwiOiJqemNrdStPcWQyeFg5YWlDWTZDT3VlMzlMOVpNdzY2Yy9kZVRXdUJqbjBSeDZqdWZ5alkzMSt5Nno4ZWZzcGJKIiwibmJmIjoxNjg2OTM3Mzc4LCJleHAiOjE2ODY5NDMzNzgsImlhdCI6MTY4NjkzNzM3OH0.9xAdQE0OYcyZZuc5Z-44uptFpvvXpbasw8LRgWCu5Do",
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
                    "loginUser": "temp37373737@gmail.com",
                    "dialCode": "1",
                    "contactNumber": "7329070930",
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
                Authorize: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiSW5kaXZpZHVhbCIsInVzZXJJZCI6InYxL282QjN6YU1Sd1JsMzY5S2hzNG9qY0hrN1RrSjRwVFNNL1FKbmZhSFE9IiwiZW1haWwiOiJqemNrdStPcWQyeFg5YWlDWTZDT3VlMzlMOVpNdzY2Yy9kZVRXdUJqbjBSeDZqdWZ5alkzMSt5Nno4ZWZzcGJKIiwibmJmIjoxNjg2OTM3Mzc4LCJleHAiOjE2ODY5NDMzNzgsImlhdCI6MTY4NjkzNzM3OH0.9xAdQE0OYcyZZuc5Z-44uptFpvvXpbasw8LRgWCu5Do
                
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

### Analyzed call stack (kobi):
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

