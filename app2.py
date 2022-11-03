from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.aik73au.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')  # 응~ 주소 뒤에 ('/')가 있으면 내가 응답할거야~~
def home():
    return render_template('home.html')


@app.route('/jaewon')
def infoJaewon():
    return render_template('/info-jaewon/index.html')


@app.route('/minseon')
def infoMinseon():
    return render_template('/info-minseon/index.html')


@app.route('/hyogeun')
def infoHyogeun():
    return render_template('/info-hyogeun/index.html')


@app.route('/dongkyun')
def infoDongkyun():
    return render_template('/info-dongkyun/index.html')


@app.route('/guest-book')
def infoGuestBook():
    return render_template('/guest-book.html')


# 디비에 방명록 데이터 넣기
@app.route('/guest-book', methods=["POST"])
def guestBook():
    name_receive = request.form['name_give']
    password_receive = request.form['password_give']
    contents_receive = request.form['contents_give']
    date_receive = request.form['date_give']
    gstbook_index = list(db.guestbookTest.find({}, {'_id': False}))
    gstbook_ID = len(gstbook_index) + 1

    doc = {
        'index': gstbook_ID,
        'name': name_receive,
        'password': password_receive,
        'contents': contents_receive,
        'date': date_receive,

    }
    # 연습이니까 일단 guestbookTest에 넣음
    db.guestbookTest.insert_one(doc)
    print(doc)
    return jsonify({'msc': '방명록 등록 완료'})


# 디비에서 방명록 조회하기
@app.route('/guest-book-2', methods=["GET"])
def guest_book_get():
    gstbook_list = list(db.guestbookTest.find({}, {'_id': False}))
    return jsonify({'list': gstbook_list})

# 방명록 삭제하기
@app.route('/guest-book-3', methods=["POST"])
def guest_book_remove():
    name_receive = request.form['name_give']
    password_receive = request.form['password_give']
    contents_receive = request.form['contents_give']
    date_receive = request.form['date_give']
    gstbook_index = list(db.guestbookTest.find({}, {'_id': False}))
    gstbook_ID = len(gstbook_index) + 1

    doc = {
        'index': gstbook_ID,
        'name': name_receive,
        'password': password_receive,
        'contents': contents_receive,
        'date': date_receive,

    }
    # 연습이니까 일단 guestbookTest에 넣음
    db.guestbookTest.insert_one(doc)
    print(doc)
    return jsonify({'msc': '방명록 등록 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
