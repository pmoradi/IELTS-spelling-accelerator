import requests
import re
from tqdm import tqdm
import pandas as pd
import os
import shutil
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR)

def download(url, file_name):
    cookies = {
        'preferredDictionaries': 'english,english-french,french-english,british-grammar',
        'XSRF-TOKEN': '8c6eca77-8979-4a44-a3de-6b789502ee92',
        'amp-access': 'amp-sNF067mSvbUnZ-G50i5wDg',
        'iawpvccs': '1',
        'iawsc1m': '1',
        'iawpvc': '1',
        'iawpvtc1m': '1',
        '_pbjs_userid_consent_data': '3524755945110770',
        '_sharedID': 'acfc3487-e66d-4f30-b017-4425be9ff04f',
        '_lr_retry_request': 'true',
        '_lr_env_src_ats': 'false',
        'OptanonConsent': 'isGpcEnabled=1&datestamp=Wed+Mar+08+2023+21^%^3A02^%^3A24+GMT^%^2B0330+(Iran+Standard+Time)&version=202211.2.0&hosts=&groups=C0001^%^3A1^%^2CC0002^%^3A0^%^2CC0003^%^3A0^%^2CC0004^%^3A0^%^2CSTACK42^%^3A0',
        'iawppid': 'a7e77163927f4546a6d7d4f848d436fc',
        'iawpvc1m': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': 'preferredDictionaries=english,english-french,french-english,british-grammar; XSRF-TOKEN=8c6eca77-8979-4a44-a3de-6b789502ee92; amp-access=amp-sNF067mSvbUnZ-G50i5wDg; iawpvccs=1; iawsc1m=1; iawpvc=1; iawpvtc1m=1; _pbjs_userid_consent_data=3524755945110770; _sharedID=acfc3487-e66d-4f30-b017-4425be9ff04f; _lr_retry_request=true; _lr_env_src_ats=false; OptanonConsent=isGpcEnabled=1&datestamp=Wed+Mar+08+2023+21^%^3A02^%^3A24+GMT^%^2B0330+(Iran+Standard+Time)&version=202211.2.0&hosts=&groups=C0001^%^3A1^%^2CC0002^%^3A0^%^2CC0003^%^3A0^%^2CC0004^%^3A0^%^2CSTACK42^%^3A0; iawppid=a7e77163927f4546a6d7d4f848d436fc; iawpvc1m=1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
    }

    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )

    with open(file_name, 'wb') as f:
        f.write(response.content)
    return True

def save_voice(word, name=None, pron='UK'):
    file_name = name or f'./voices/{word}.mp3'
    if os.path.isfile(file_name):
        return

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,af;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.3.1152551443.1666262491; amp-access=amp-6WbD_iy59OSC5zZX4XNwMA; preferredDictionaries="english,british-grammar,english-arabic,english-turkish"; OptanonAlertBoxClosed=2022-10-20T10:41:38.919Z; OTAdditionalConsentString=1~39.61.70.89.93.108.122.124.131.136.143.144.147.149.159.162.167.171.192.196.202.211.218.228.230.239.241.259.266.272.291.311.317.323.326.338.371.385.389.394.397.407.413.415.424.430.436.449.482.486.491.494.495.505.522.523.540.550.559.568.574.576.584.591.737.745.787.802.803.817.820.821.829.839.864.874.899.922.981.1051.1095.1097.1201.1205.1211.1276.1301.1365.1415.1449.1570.1577.1651.1716.1765.1870.1878.1889.2008.2072.2074.2202.2253.2299.2322.2328.2357.2465.2501.2526.2568.2571.2575.2677.2999.3028.3225.3226.3231.3232.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300.3306.3307.3308.3314.3315.3316.3318.3324.3327.3328.3330; iawppid=6ddfd04aa9c94c34922b3f9bda3c1324; _hjSessionUser_2790984=eyJpZCI6IjEyZDRiYTAxLThhMzktNWUzOC05MTUzLWJlMmMzNmJmY2FjNCIsImNyZWF0ZWQiOjE2NjY2Mjc1Nzg2MDMsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1666628281594.819635154; __gads=ID=a1b4c36c85df77c3:T=1666262501:S=ALNI_MaBJUju-4nUlYifsXm2BKpvHislRA; _lr_env_src_ats=false; iawpvc1m=1; _sharedID=acf4d12d-16ed-4a62-b2c6-b91446d8f485; pbjs-unifiedid=%7B%22TDID%22%3A%22909c0abe-8005-4b11-8143-30b6aa033149%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-01-19T16%3A34%3A30%22%7D; _tfpvi=ZjIzNTg1MjAtZjE2Mi00OTIzLWI2NjMtYjc4Y2YzNGJkY2ZlIy05MA%3D%3D; eupubconsent-v2=CPhI67QPhI67QAcABBENC6CsAP_AAH_AAChQHQpD7T7FYSnC-PZ5fLsAcAhHR9TkA6QACASAAmABAAKQIIQCkmAYlASgBAgCAAAgAAJBAAIECAEACUAAwAAAAQAEAAAABAAIACAAgAARAgAICAACAAAAAAAIgAAAEAAAmwgAQIIACEgABAAAAAAAAAgAAAAAAgdjAiAAWAA8ACoAFwAMwAbABwAEAAJAAZAA0AByAD8AKwAfgBCACOAEwAKMAUoBCACIgEdAMCAZ8A14BxIDpAOoAeQA-QCLwExAMEAZYA7EBIJATAB5AEMARQAmABPACqAFiARABEgClAFuAMMAewA_QCBgEcAKeAYoBSIC8wGThAAgAiwBqAI9AU2GACgBPAEWANQA2QCmw0AMAp4CkQGTiAAYATwBFgDUEQAwCngKRAZOKgCABDACYARwBeYoAEANQBHoyAIAEMAJgBHAF5jAAQA1AEejoDIAPAAfQBDAEUAJgATwAqgBYAC6AGKARABEgClAFuAMMAaIA9gB-gEDAIsARwAp4BigF5gL6AZOAywcAFAC-ANQArICPQFNkIBAAQwAmABVADEARwAp4BigGTkAAgAXwBqAFZAR6SgHAA8ACIAEwAKoAYoBEAESAKUAW4BHACngGKAXmAycBlhIAGANQArICPSkBMAHkAQwBFACYAE8AKQAVQAsABigEQARIApQBbgDRAH6ARYAjgBigF5gL6AZOUACgBfAGoAVkBHoCmwA.f_gAD_gAAAAA; __gpi=UID=00000b75aaabf4af:T=1666262501:RT=1677944962:S=ALNI_MYMOCsVYAIyVdbOL0eLWHAP6Yu3-g; _pbjs_userid_consent_data=579596144183168; iawpvccs=1; iawsc1m=14; iawpvc=332; iawpvtc1m=60; cto_bidid=xiWndV9RM2NQbXIycXRYOWVQWWgzbU9SUHBoeUR4d000TiUyRnA5Z3lTcm5yVE5qRkpYMEQlMkI0blV5VWdtSFVLQVdZbmdiOTRTNSUyQmIlMkZobFZaJTJGamdycXU1SkxlYVB3VU5HVVpRQlRLZkhhM2JjZDRraHMlM0Q; cto_bundle=QLq6a194ZG9udHBEWTVnVzdveCUyQmNLV1ExdllHTlpZQlZCelc0V1dpTUhJZ3JheWNaVzdMdm83aG1ubkY4WkZHSk5RRyUyRmlVVTIlMkJlcVRYUUVla0tHd2dXa2R4YW1mT1FBUE9UbjlmYzUlMkJKQ2FkOGJUQjR4RU9GMnd2dUxmcVVJUFhNSTNCeXZGYkI3aHF3RmtJajRSZ283RDh5dyUzRCUzRA; XSRF-TOKEN=8c2422d4-7091-4f0a-a376-43e2a267b852; _gid=GA1.3.1544053118.1678294093; loginPopup=2; _hjIncludedInSessionSample_2790984=0; _hjSession_2790984=eyJpZCI6ImRiZmUzYmRlLTBjZmYtNDYyNi05YTkwLWY5N2U1ZDllMjA5OSIsImNyZWF0ZWQiOjE2NzgyOTQxMzI0MDQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga_L9GCR21SZ7=GS1.3.1678294093.95.1.1678294423.0.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+08+2023+20%3A23%3A43+GMT%2B0330+(Iran+Standard+Time)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=a5afaba6-5e9e-4dff-9aee-d3f4b07d61a9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=DE%3BNW&AwaitingReconsent=false',
        # 'Referer': 'https://dictionary.cambridge.org/dictionary/english/beat-a-retreat',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(f'https://dictionary.cambridge.org/dictionary/english/{word}', headers=headers)
    data = response.text

    data = data.split('\n')
    for l in data:
        if '.mp3' in l and ((pron=='UK' and '/english/uk_pron/' in l) or (pron=='US' and '/english/us_pron/' in l)) :
            line = l
            break
    left, right = re.search(r'src=".+"', line).span()
    left += 5
    right -= 1
    file_address = line[left:right]
    file_address = 'https://dictionary.cambridge.org' + file_address 
    if name is None:
        download(file_address, f'./voices/{word}.mp3')
    else:
        download(file_address, f'./voices/{name}.mp3')

def remove_files_with_size(path, size):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and os.path.getsize(file_path) == size:
            os.remove(file_path)
            print(f"{file_path} removed")


def check_files(pron='US'):
    files = os.listdir('./voices')
    files = [f for f in files if '.mp3' in f]
    test_file = 'booookss'
    if os.path.isfile(f'voices/suspecious_files/{test_file}.mp3'):
        os.remove(f'voices/suspecious_files/{test_file}.mp3')
    save_voice(test_file, name=f'suspecious_files/{test_file}', pron=pron)
    test_fs = os.path.getsize(f'./voices/suspecious_files/{test_file}.mp3')

    for f in files:
        fs = os.path.getsize(f'./voices/{f}')
        if fs == test_fs:
            shutil.move(f'./voices/{f}', f'./voices/suspecious_files/{f}')

if __name__ == "__main__":
    # words = ['career']
    word = pd.read_csv('./data/word_list.csv')['word']
    word = list(word)
    for w in tqdm(word):
        try:
            save_voice(w, pron='US')
        except:
            logging.error(w)
    # remove_files_with_size('./voices', size)
    # check_files()