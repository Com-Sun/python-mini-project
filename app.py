from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Server
client = MongoClient('localhost', 27017)
db = client.comsun
app = Flask(__name__)


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/comsec', methods=['GET'])
def comsec_read():
    result = list(db.comsec.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'card': result})


@app.route('/comsec', methods=['POST'])
def comsec_post():
    # 클라이언트로부터 데이터 받기
    comsec_receive_temp = request.form['comsec_give']
    url = ('https://search.naver.com/search.naver?where=view&sm=tab_jum&query=')
    comsec_receive = (url + comsec_receive_temp)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36 '
    }
    data = requests.get(comsec_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    views = soup.select('#main_pack > section > div > div._list > panel-list > div > more-contents > div > ul '
                        '> li > div.total_wrap.api_ani_send')
    for i in views:
        # img
        img_tag = i.select_one('a.thumb_single > span > img')
        if img_tag is not None:
            img = img_tag['src']
            a_tag = i.select_one('div.total_area > a')

            # title
            title = a_tag.text

            # link
            link = a_tag['href']

            # description
            desc_tag = i.select_one('div.total_area > div.total_group > div > a > div')
            desc = desc_tag.text
            card = {'link': link, 'title': title, 'desc': desc, 'img': img}
            print(card)
            db.comsec.insert_one(card)

    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})


@app.route('/comsec/delete', methods=['GET'])
def comsec_delete():
    db.comsec.drop()

    return jsonify({'result': 'success', 'msg': 'DB가 삭제되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
