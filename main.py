import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def getcouselist():
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
    li=[]
    for i in courselist:
        try:
            yearnumber = (i.text).split(' ')[0]
            if len(yearnumber) == 4 and '111' in yearnumber and ('[' in i.text) and (']' in i.text):
                # print(i.text,end="\t")
                # print(i.text[-5:-1])
                li.append(i.text[-5:-1])
        except:
            pass
    return li

def getcoursedetail(coursenumber):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    json_data = {
        "baseOptions": {
            "lang": "cht",
            "year": 111,
            "sms": 1
        },
        "typeOptions": {
            "code": {
                "enabled": 'true',
                "value": coursenumber
            },
            "weekPeriod": {
                "enabled": 'false',
                "week": "*",
                "period": "*"
            },
            "course": {
                "enabled": 'false',
                "value": ""
            },
            "teacher": {
                "enabled": 'false',
                "value": ""
            },
            "useEnglish": {
                "enabled": 'false'
            },
            "useLanguage": {
                "enabled": 'false',
                "value": "01"
            },
            "specificSubject": {
                "enabled": 'false',
                "value": "1"
            },
            "courseDescription": {
                "enabled": 'false',
                "value": ""
            }
        }
    }
    url = 'https://coursesearch01.fcu.edu.tw/Service/Search.asmx/GetType2Result'
    data = requests.post(url, headers=headers, json=json_data)
    data = data.text.replace('\\','').replace('"{','{').replace('}"','}')
    data = json.loads(data)['d']['items'][0]['scr_period']
    return data

finalcourselist = {
    '一':{1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:'',10:'',11:'',12:'',13:''},
    '二':{1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:'',10:'',11:'',12:'',13:''},
    '三':{1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:'',10:'',11:'',12:'',13:''},
    '四':{1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:'',10:'',11:'',12:'',13:''},
    '五':{1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:'',10:'',11:'',12:'',13:''}
}
def parasecoursetime(detail , classnumber):
    daylist=['一','二','三','四','五']
    data = detail.split('(')
    for i in data:
        try:
            if(i[0] in daylist):
                time = i.split(' ')
                # print(time)
                try:#如果連續兩節以上
                    duotime = time[0].split('-')
                    # print(int(duotime[0][-2:]),int(duotime[1]))
                    for t in range(int(duotime[0][-2:]),int(duotime[1])+1):
                        # print(t)
                        finalcourselist[i[0]][t] = classnumber
                except:#單節
                    finalcourselist[i[0]][int(time[0][-2:])] = classnumber
        except:
            pass
    print(detail , classnumber)

if __name__ == '__main__':
    load_dotenv()
    courselist = getcouselist()
    print('課程清單:')
    print(courselist,end='\n\n')

    print('課程時間:')
    for i in courselist:
        coursedetail = getcoursedetail(i)
        parasecoursetime(coursedetail , i)
    
    print('\n課表(json):')
    print(finalcourselist)

    #to excel
    df = pd.DataFrame(finalcourselist)
    df.to_excel('result.xlsx')