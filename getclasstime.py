import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    cookies = {
        '_ga_G4F1Y2399J': 'GS1.1.1659795430.1.1.1659797511.59',
        '_fbp': 'fb.2.1663209926219.1941752656',
        '_ga_Z2D58ZW6BJ': 'GS1.1.1665707406.1.1.1665707481.60.0.0',
        '_ga_R7R8BG5V75':'GS1.1.1667543230.4.0.1667543230.60.0.0',
        '_ga_Q6H219D03D':'GS1.1.1667543230.4.0.1667543230.60.0.0',
        '_gid':'GA1.3.347861270.1670821320',
        '_ga':'GA1.3.231169675.1649209207',
        '_gat':'1',
        
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://coursesearch02.fcu.edu.tw',
        'Pragma': 'no-cache',
        'Referer': 'http://service005.sds.fcu.edu.tw/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'id': os.getenv('username'),
        'password': os.getenv('pw'),
        'baseOptions': {
            'lang': 'cht',
            'year': 111,
            'sms': 1,
        }
    }

    response = requests.post('https://coursesearch02.fcu.edu.tw/Service/Auth.asmx/login', cookies=cookies, headers=headers, json=json_data)
    print(response.text)

