#!/usr/bin/env python
__filename = 'kobi_gather_res.py'
__fname = 'kobi_gather_res'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')
'''
    house_061323:
        create regex to filter uri params for 'https://visa.vfsglobal.com/x1/x2/x3'
        - there are 1152 unique urls... len(unique_matches): 1152
'''
#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import json
import os
import re

#------------------------------------------------------------#
#   PROCEDURAL SUPPORT                                       #
#------------------------------------------------------------#
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
