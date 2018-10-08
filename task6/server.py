from flask import Flask,request,jsonify,Response
import functools
from pymongo import MongoClient
from bson.json_util import dumps

# Importing Database configurations
from config import HOST,PORT,DB

app = Flask(__name__)

# connecting to mongoDB
con = MongoClient(HOST, PORT)

# accesing DB
db = con.DB

# getting reference to collections
logs = db.calculations
lastlogs = db.latest_operations

# Task6 Part 1
# logrequest : a funtion to store incoming requests to mongodb logs
def logrequest(data, ans):
    data['result'] = ans
    logs.insert_one(data)
    print("Logged req : {0}".format(data))
    recentlog(data)

# Task6 Part 2
# Used $push and $each,$slice,$sort modifiers in combination to log only 4 recent
# requests of each type of operation
# last_operations collection structure : 
#   {
#       { "op": '+',
#         "logs": [
#                    {'op':'+', 'op1':7, 'op2':3, 'result':10, "_id":{"$oid": ObjectID(2AB3..)}}
#                 ]
#       }
#       { "op": '-',
#         "logs": [
#                    {'op':'-', 'op1':7, 'op2':3, 'result'4:, "_id":{"$oid": ObjectID(2YI3..)}}
#                 ]
#       }
#   }
def recentlog(data):
    print("req object at /recentlogs",data)
    try:
        if lastlogs.find_one({"op": data["op"]}) is None:
            print("{0} is accessed for the first time".format(data['op']))
            insertDoc = {
                "op": data['op'],
                "logs": [data]
            }
            lastlogs.insert_one(insertDoc)
        else:
            # Golden query :) To keep only recent 4 logs of each 'op' type
            lastlogs.update_one({"op":data['op']}, { "$push": { "logs" : { "$each": [data], "$sort": { "_id": -1 }, "$slice": 4 } }})
    except:
        print("Error in inserting doc to lastlogs collection")


# simple hello world route for testing
@app.route("/")
def hello_world():
    return 'Hello Task6'

# calculator_api helper function
# Input: (2,5,'+')
# Output: 7
def calculate(op1,op2,op):
    if op == "+":
        return op1+op2
    if op == "-":
        return op1-op2
    if op == "*":
        return op1*op2
    if op == "/":
        return op1/op2
    else:
        return "Invalid Operation"

# calculator endpoint supporting +,-,*,/ with two operands
# input data and response format is JSON
@app.route("/calc", methods=['POST'])
def calculator_api():
    try:
        data = request.json
        print(data)
        op = data["op"]
        op1 = data["op1"]
        op2 = data["op2"]


        ans = calculate(op1,op2,op)
        resp = {"result": ans}
        # save request to mongodb logs
        logrequest(data,ans)
    except:
        resp = {"result": "Bad json object"}

    return jsonify(resp)

# Helper function
# Get all docs and return as a list
def getAllDocs(collection):
    doclist = []
    cursor = collection.find({},{"_id":0})
    for doc in cursor:
        doclist.append(doc)
    return doclist

# Task6 Part 3
@app.route("/calculations", methods=['GET'])
def get_logs():
    loglist = getAllDocs(logs)
    count = logs.count()
    loglist.append("total_records:{0}".format(count))
    return Response(dumps(loglist), mimetype='application/json')

# Task6 Part 2
@app.route("/recentlogs", methods=['GET'])
def get_recent_logs():
    rloglist = getAllDocs(lastlogs)
    return Response(dumps(rloglist), mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
