from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pennapps'
app.config['MONGO_URI'] = 'mongodb://admin:password@ds263837.mlab.com:63837/pennapps'

mongo = PyMongo(app)


@app.route("/addLottery", methods=['POST'])
def add_lottery():
    lotteries = mongo.db.lotteries
    lotteries.insert_one(
        {'title': request.args.get("name"), 'total': request.args.get("amount"), 'endtime': request.args.get("endtime"),
         'participants': {request.args.get("ID"): request.args.get("amount")}})
    return jsonify({'result': request.args})


@app.route('/getLotteries', methods=['GET'])
def get_all_articles():
    lotteries = mongo.db.lotteries

    output = []
    for q in lotteries.find():
        output.append({'title': q['title'],
                       'total': q['total'],
                       'participants': q['participants']})

    return jsonify({'result': output})


@app.route("/")
def home():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
