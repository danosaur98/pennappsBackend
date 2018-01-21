import uuid
import random

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pennapps'
app.config['MONGO_URI'] = 'mongodb://admin:password@ds263837.mlab.com:63837/pennapps'

mongo = PyMongo(app)


@app.route("/addLottery", methods=['POST'])
def add_lottery():
    lotteries = mongo.db.lotteries
    lotteryID = str(uuid.uuid4())
    lotteries.insert_one(
        {'lotteryID': lotteryID, 'title': request.args.get("name"), 'total': request.args.get("total"),
         'charity': request.args.get("charity"), 'endDate': request.args.get("endDate"),
         'participants': {request.args.get("participantID"): request.args.get("total")}})
    return jsonify({'result': lotteryID})


@app.route('/getLotteries', methods=['GET'])
def get_lotteries():
    lotteries = mongo.db.lotteries

    output = []
    for q in lotteries.find():
        output.append({'lotteryID': q['lotteryID'],
                       'title': q['title'],
                       'total': q['total'],
                       'participants': q['participants'],
                       'charity': q['charity'],
                       'endDate': q['endDate']})

    return jsonify({'result': output})


@app.route('/joinLottery', methods=['POST'])
def join_lottery():
    lotteries = mongo.db.lotteries
    l = lotteries.find_one({'lotteryID': request.args.get('lotteryID')})
    participants = l['participants']
    participants[request.args.get('participantID')] = request.args.get('contribution')
    total = str(int(l['total']) + int(request.args.get('contribution')))
    lotteries.update(
        {"lotteryID": request.args.get('lotteryID')},
        {
            '$set': {
                'participants': participants,
                'total': total
            }
        }
    )
    output = "Successfully joined!"
    return jsonify({"result": output})


@app.route('/decideWinner', methods=['GET'])
def decide_winner():
    lotteries = mongo.db.lotteries
    l = lotteries.find_one({'lotteryID': request.args.get('lotteryID')})
    participants = l['participants']
    total = int(l['total'])
    winning_number = random.randint(0, total)
    winner = ""
    summed = 0
    for p in participants:
        if summed < winning_number <= summed + int(participants[p]):
            winner = p
            break
        else:
            summed += int(participants[p])
    amountWon = round(0.95 * total, 2)
    amountDonated = round(0.05 * float(participants[request.args.get('participantID')]), 2)
    output = {"winner": winner, "amountWon": amountWon, "amountDonated": amountDonated}
    return jsonify(output)


@app.route('/getFunds', methods=['GET'])
def get_funds():
    users = mongo.db.users
    u = users.find_one({'participantID': request.args.get('participantID')})
    output = {"bank": u['bank'], "donated": u['donated']}
    return jsonify(output)

@app.route('/updateFunds', methods=['POST'])
def update_funds():
    users = mongo.db.users
    u = users.find_one({'participantID': request.args.get('participantID')})
    new_bank_amount = str(u['bank'] + float(request.args.get('bankToBeAdded')))
    new_donated_amount =  str(u['bank'] + float(request.args.get('donatedToBeAdded')))
    users.update(
        {"participantID": request.args.get('participantID')},
        {
            '$set': {
                'bank': new_bank_amount,
                'donated' : new_donated_amount
            }
        }
    )
    output = {}
    return jsonify(output)


@app.route("/")
def home():
    return "Ayy lmao!"


if __name__ == '__main__':
    app.run(debug=True)
