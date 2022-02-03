from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# open API
import urllib.request
client_id = "R8kWOPeafPnDEV9L_CIj"
client_secret = "Lwcj1_xJlJ"

# API body
url = "https://openapi.naver.com/v1/search/blog"
query = "?query=" + urllib.parse.quote("랑그릿사")
option = "&display=1"
url_query = url + query + option  # json 결과

## API 검색 요청 개체 설정
request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

## 검색 요청 및 처리
response = urllib.request.urlopen(request)
rescode = response.getcode()
if (rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

# Server
client = MongoClient('localhost', 27017)
db = client.comsun
app = Flask(__name__)


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def read_list():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.comsec.find({}, {'_id': False}))

    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result': 'success', 'articles': result})


# API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_list():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give']

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36 '
    }
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_title = og_title['content']
    url_description = og_description['content']
    url_image = og_image['content']

    article = {'url': url_receive, 'title': url_title, 'desc': url_description, 'img': url_image}

    # 3. mongoDB에 데이터 넣기
    db.comsec.insert_one(article)

    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
