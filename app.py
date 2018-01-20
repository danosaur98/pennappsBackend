import uuid

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
        {'lotteryID': str(uuid.uuid4()), 'title': request.args.get("name"), 'total': request.args.get("amount"),
         'endtime': request.args.get("endtime"),
         'participants': {request.args.get("participantID"): request.args.get("amount")}})
    return jsonify({'result': request.args})


@app.route('/getLotteries', methods=['GET'])
def get_lotteries():
    lotteries = mongo.db.lotteries

    output = []
    for q in lotteries.find():
        output.append({'lotteryID': q['lotteryID'],
                       'title': q['title'],
                       'total': q['total'],
                       'participants': q['participants']})

    return jsonify({'result': output})


@app.route('/joinLottery', methods=['POST'])
def joinLottery():
    lotteries = mongo.db.lotteries
    l = lotteries.find_one({'id': request.args.get('id')})
    participants = l['participants']
    participants[request.args.get('participantID')] = request.args.get('contribution')
    lotteries.update(
        {"id": request.args.get['id']},
        {
            '$set': {
                'participants' :participants
            }
        }
    )


@app.route("/")
def home():
    return "Ayy lmao!"


if __name__ == '__main__':
    app.run(debug=True)
