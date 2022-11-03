from flask import Flask, render_template, request, jsonify

import time
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
    today_time = time.strftime("%Y-%m-%d")
    # date_receive = request.form['date_give']
    gstbook_index = list(db.guestbookTest.find({}, {'_id': False}))
    gstbook_ID = len(gstbook_index) + 1

    doc = {
        'index': gstbook_ID,
        'name': name_receive,
        'password': password_receive,
        'contents': contents_receive,
        'date' : today_time
        #'date': date_receive,
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

#화면에받아올 데이터를 보여주기 위한 검색 class
@app.route("/guest-book-comment1", methods=["GET"])
def guestBookCommentsGet():
    comment_list = list(db.comments.find({}, {'_id':False}))
    return jsonify({'comments': comment_list})
    #print(comment_list)
    #return render_template('/templates/guest-book.html', comments=comment_list)

#삭제의 고유넘버를 받아오기 위한 검색class
def guestBookCommentsFind(data):
    #comment = db.comments('no').find({data})
    print(list(db.comments.find({}, {'_id':False})))
    comment = list(db.comments.find({'cno':int(data)}, {'_id':False}))
    return comment[0]['password']

#삭제하기위한 class
@app.route("/guest-book-commentRemove", methods=["POST"])
def guestBookCommentsDel():
    password_receiver = request.form['password_give']
    del_receiver = request.form['del_give']
    # comment = list(db.comments.find({'no':int(data)}, {'_id':False}))
    # comment[0]['password']
    # if password_receiver == guestBookCommentsFind(del_receiver):
    if password_receiver == guestBookCommentsFind(del_receiver):
        db.comments.delete_one({'cno':int(del_receiver)})
        return jsonify({'msg':"삭제가 완료었습니다"})
    else :
        return jsonify({'msg':'비밀번가 틀렸습니다'})

#데이터 베이스(DB)에 html에서받은 데이터 입력
@app.route("/guest-book-commentIn", methods=["POST"])
def guestBookCommentsIn():
    name_comment_receive = request.form['name_comment_give']
    password_comment_receive = request.form['password_comment_give']
    contents_comment_receive = request.form['contents_comment_give']
    # book_comment_no_receive = request.form['book_no_comment_give']
    today_comment_time = time.strftime("%Y-%m-%d")
    count_comment = list(db.bucket.find({},{'_id':False}))
    num_comment = len(count_comment) + 1
    cno_comment = len(count_comment) + 1
    doc ={
        'num':num_comment,
        'cno':cno_comment,
        'name':name_comment_receive,
        'password':password_comment_receive,
        'content':contents_comment_receive,
        'date':today_comment_time
    }
    db.comments.insert_one(doc)
    return jsonify({'msg':'등록 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
