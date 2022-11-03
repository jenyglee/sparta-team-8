from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.aik73au.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# 팀원들께 알림니다. 제가 코드 분석하면서 이해가기 쉬우라고 적어놓은 주석들은
# 머리에서 나오는 의식의 흐름대로 적기 때문에 모두 반말입니다.. 양해 부탁드립니다..♡

@app.route('/')  # 응~ 주소 뒤에 ('/')가 있으면 내가 응답할거야~~
def home():
    return render_template('home.html')


# 나는 render_template()안의 데이터들을 가지고 올거야~~ 불러올거야~~


# 재원 자기소개 페이지 렌더(?리다이렉트..?)
@app.route('/jaewon')
def infoJaewon():
    return render_template('/info-jaewon/index.html')


# 민선 자기소개 페이지 렌더(?리다이렉트..?)
@app.route('/minseon')
def infoMinseon():
    return render_template('/info-minseon/index.html')


# 효준 자기소개 페이지 렌더(?리다이렉트..?)
@app.route('/hyogeun')
def infoHyogeun():
    return render_template('/info-hyogeun/index.html')


# 동근 자기소개 페이지 렌더(?리다이렉트..?)
@app.route('/dongkyun')
def infoDongkyun():
    return render_template('/info-dongkyun/index.html')


# 방명록 페이지 렌더(?리다이렉트..?)
@app.route('/guest-book', methods=["POST"])
# 주소에 게스트 북이 오면 내가 응답할거야~~ 나는 포스트로 비밀리에 데이터들을 가져올거야~~
def guestBook():

    # guest-book 페이지에서 비밀리에[POST]로 가져온 name_give 데이터를 name_receive 변수에 넣어줄거야~~
    # 그렇다면 여기서 우리가 필요한 데이터들을 일단 모두 가져와서 변수에 넣어주어야겠네~~
    # name_receive = request.form['name_give']
    # password_receive = request.form['password_give']
    # contents_receive = request.form['contents_give']
    # date_receive = request.form['date_give']
    # gstBook_list = list(db.bucket.find({}, {'_id': False}))
    # gstBook_ID = len(gstBook_list) + 1

    # 1. 파인드로 디비에서 인덱스아이디를 찾자~~ >> 얘 1번

    # form에서 가져올 수 있는 데이터는 4개밖에 없어. index는 등록 되어지는 것을 COUNT 해서 변수에 따로 넣어줘야 해
    # --------------------------- 인덱스 변수 넣을 예정 ----------------------------

    # 변수에 넣어준 애들을 디비에 넣자~~~

    # doc = {
    #     'index': gstBook_ID,
    #     'name': name_receive,
    #     'password': password_receive,
    #     'contents': contents_receive,
    #     'date': date_receive,
    #
    # }
    # #이런 데이터들을 넣을거야~~ index에는 gstBook_ID에 있는 변수값을 넣을거야~~
    # db.guestbook.insert_one(doc)
    # print(doc)
    return render_template('guest-book.html')
    # 그리고 나는(guestBook함수) 리턴할꺼야~~ (다시 보내줄거야~~) 데이터들을
    # 'guest-book.html'한테 다시 보내줄거야~~~


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
