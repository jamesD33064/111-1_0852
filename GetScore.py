import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import requests

def getscore():
    url = 'https://ilearn2.fcu.edu.tw/'

    username = os.getenv('username')
    pw = os.getenv('pw')
    login_data = {
        'username': username,
        'password': pw,
        'anchor':'', 
        'logintoken': ''
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }
    session = requests.Session()
    response = session.get(url)

    parser = BeautifulSoup(response.text, 'lxml')
    login_data['logintoken'] = parser.select("#login > input[type=hidden]")[0]['value']
    print(login_data['logintoken'])
    response = session.post("https://ilearn2.fcu.edu.tw/login/index.php",data=login_data,headers=headers)
    if "我的課程" in response.text :
        try:
            print("登入成功")
            course_url="https://ilearn2.fcu.edu.tw/course/view.php?id="
            try:
                split_data = []
                for i in range(1,100):
                    split_data.append(response.text.split("coc-course-")[i].split('"')[0])
            except:
                pass
            score_url_list=[]
            for course_id in split_data:
                try:
                    response = session.get(course_url+course_id,headers=headers)
                    parser = BeautifulSoup(response.text, 'lxml')
                    score_url = parser.select("#inst36323 > div.content > ul > li:nth-child(9) > div > a")[0]['href']
                    score_url_list.append(score_url)
                    response = session.get(score_url,headers=headers)
                    parser = BeautifulSoup(response.text, 'lxml')
                    course_name = parser.select("#CourseName")[0].text
                    final_score = parser.select("#final_score")[0].text
                    # if '未' in final_score :
                    #     continue 
                    print("----------------------------------------------------")
                    print(course_name)
                    print(final_score)
                except:
                    pass
        except:
            print("可憐_1")
    else:
        print("可憐_2")


if __name__ == '__main__':
    load_dotenv()
    courselist = getscore()