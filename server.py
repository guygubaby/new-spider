from flask import Flask, jsonify, request
from utils.mongodb import emoji_db

app = Flask(__name__)


class Result:
    def __init__(self):
        pass

    @staticmethod
    def ok(data=None):
        return jsonify({'code': 0, 'data': data})

    @staticmethod
    def error(data=None):
        return jsonify({'code': -1, 'data': data})


@app.route('/')
def index():
    return 'pong'


@app.route('/api/emoji')
def get_emoji():
    res = []
    args = request.args
    page = args.get('page', 0)
    size = args.get('size', 10)
    _list = emoji_db.find().skip(int(page) * int(size)).limit(int(size))
    for item in _list:
        item['_id'] = str(item['_id'])
        res.append(item)
    return Result.ok(res)


if __name__ == '__main__':
    app.run(debug=True)
