import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()
username = os.getenv('username')
pw = os.getenv('pw')

login_data={
    'username': username,
    'password': pw,
    'anchor':'', 
    'logintoken': ''
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
}
url = 'https://ilearn2.fcu.edu.tw/'
session = requests.Session()
response = session.get(url)
parser = BeautifulSoup(response.text, 'lxml')
login_data['logintoken'] = parser.select("#login > input[type=hidden]")[0]['value']

response = session.post("https://ilearn2.fcu.edu.tw/login/index.php",data=login_data,headers=headers)
parser = BeautifulSoup(response.text, 'lxml')
courselist = parser.select('ul.nav li.dropdown div.dropdown-menu ul li a')
# print(courselist[0].text)

for i in courselist:
    try:
        if len((i.text).split(' ')[0]) == 4:
            print(i.text)
            print()
    except:
        pass