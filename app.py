from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('민선님 몽고디비 주소')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jaewon')
def infoJaewon():
    return render_template('info-jaewon/index.html')

@app.route('/guest-book')
def guestBook():
    return render_template('guest-book.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
