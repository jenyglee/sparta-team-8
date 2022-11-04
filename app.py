from flask import Flask, render_template, request, jsonify

import time

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.aik73au.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
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
        'date': today_time
        # 'date': date_receive,
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


# 삭제의 고유넘버를 받아오기 위한 검색class
def guestBookGuestFind(data):
    print("data : ", data) # 11
    # comment = db.comments('no').find({data})
    # print(list(db.comments.find({}, {'_id': False})))
    comment = db.guestbookTest.find_one({'index': int(data)}, {'_id': False})
    print("comment : ", comment) # {'index': 6, 'name': '333', 'password': '3333', 'contents': '333', 'date': '2022-11-04'}
    return comment['password']

# 방명록 삭제하기
@app.route('/guest-book-3', methods=["POST"])
def guest_book_remove():
    index_receive = request.form['index_give']
    password_receive = request.form['password_give']
    all = list(db.guestbookTest.find({}, {'_id': False}))
    real_password = db.guestbookTest.find_one({'index': int(index_receive)},
                                              {'name': False, 'date': False, 'contents': False, '_id': False})
    print("all :", all)

    # all: [{'index': 2, 'name': '테스트2', 'password': 'qwer', 'contents': 'qwer', 'date': '2022-11-04'},
    #       {'index': 3, 'name': '1', 'password': 'asdf', 'contents': 'asdf', 'date': '2022-11-04'},
    #       {'index': 3, 'name': '테스트1', 'password': '1234', 'contents': '1234', 'date': '2022-11-04'},
    #       {'index': 4, 'name': '테스트2', 'password': 'qwer', 'contents': 'qwer', 'date': '2022-11-04'},
    #       {'index': 5, 'name': '이름이름', 'password': 'adad', 'contents': 'adad', 'date': '2022-11-04'},
    #       {'index': 6, 'name': '333', 'password': '3333', 'contents': '333', 'date': '2022-11-04'}] ✨

    print("index_receive :", index_receive)  # 6
    print("password_receive :", password_receive)  # 3333
    print("real_password :", real_password)  # {'index': 6, 'password': '3333'}

    # print(type(real_password['password']))
    # print(type(real_password['index']))
    # 리얼 패스워드에 리스트에 두개의 값이 저장이 될텐데.. 인덱스 값과 패스워드 값이 체크한 비밀번호 값과 같다면...

    # if password_receive == real_password['password'] and index_receive == real_password['index']:
    print("guestBookGuestFind(index_receive) :", guestBookGuestFind(index_receive)) # 3333
    if password_receive == guestBookGuestFind(index_receive):
        db.guestbookTest.delete_one({'index': real_password['index']})
        return jsonify({'msg': "삭제가 완료되었습니다."})
    else:
        return jsonify({'msg': "비밀번호가 틀렸습니다."})


# 화면에받아올 데이터를 보여주기 위한 검색 class
@app.route("/guest-book-comment1", methods=["GET"])
def guestBookCommentsGet():
    comment_list = list(db.comments.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})
    # print(comment_list)
    # return render_template('/templates/guest-book.html', comments=comment_list)


# 삭제의 고유넘버를 받아오기 위한 검색class
def guestBookCommentsFind(data):
    # comment = db.comments('no').find({data})
    print(list(db.comments.find({}, {'_id': False})))
    comment = list(db.comments.find({'cno': int(data)}, {'_id': False}))
    return comment[0]['password']


# 삭제하기위한 class
@app.route("/guest-book-commentRemove", methods=["POST"])
def guestBookCommentsDel():
    password_receiver = request.form['password_give']
    del_receiver = request.form['del_give']
    # comment = list(db.comments.find({'no':int(data)}, {'_id':False}))
    # comment[0]['password']
    # if password_receiver == guestBookCommentsFind(del_receiver):
    if password_receiver == guestBookCommentsFind(del_receiver):
        db.comments.delete_one({'cno': int(del_receiver)})
        return jsonify({'msg': "삭제가 완료었습니다"})
    else:
        return jsonify({'msg': '비밀번호가 틀렸습니다'})


# 데이터 베이스(DB)에 html에서받은 데이터 입력
@app.route("/guest-book-commentIn", methods=["POST"])
def guestBookCommentsIn():
    name_comment_receive = request.form['name_comment_give']
    password_comment_receive = request.form['password_comment_give']
    contents_comment_receive = request.form['contents_comment_give']
    # book_comment_no_receive = request.form['book_no_comment_give']
    today_comment_time = time.strftime("%Y-%m-%d")
    count_comment = list(db.comments.find({}, {'_id': False}))
    num_comment = len(count_comment) + 1
    cno_comment = len(count_comment) + 1
    doc = {
        'num': num_comment,
        'cno': cno_comment,
        'name': name_comment_receive,
        'password': password_comment_receive,
        'content': contents_comment_receive,
        'date': today_comment_time
    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
