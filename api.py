import sys

sys.path.append('util')
sys.path.append('task')

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from mongoUtil import Database
from refreshTask import tick

import json
import time


class Config(object):
    DEBUG = True
    JSON_AS_ASCII = False


app = Flask(__name__)
app.config.from_object(Config)
# 跨域访问，指定域名cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

db = Database("MONGOLAB")


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


@app.route('/device', methods=['POST'])
def device():
    if request.method == 'POST':
        result = db.insert_one("DEVICE_INFO", request.json)
        print(result)
        return jsonify(result)


@app.route('/deviceInfo', methods=['GET'])
def deviceInfo():
    result = []
    for x in db.find("DEVICE_INFO", {}):
        result.append(x)
    print(result)
    return jsonify(result)


@app.route('/deviceData', methods=['GET', 'POST'])
def deviceData():
    if request.method == 'GET':
        result = []
        for x in db.find("DEVICE_DATA_CURRENT", {}):
            result.append(x)
        print(result)
        return jsonify(result)
    if request.method == 'POST':
        deviceId = request.json.get('_id')
        timestap = request.json.get('timestap')
        st = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        mongotime = datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
        jsondata = request.json
        print(jsondata)
        jsondata['timestap'] = mongotime
        print(jsondata)

        condition = {'_id': deviceId}
        jData = {"$set": jsondata}

        db.update_data("DEVICE_DATA_CURRENT", condition, jData)
        return jsonify()


@app.route('/deviceDataDetail/<id>', methods=['GET'])
def deviceDataDetail(id):
    # paramId = request.json.get('id')
    result = []
    for x in db.find("DEVICE_DATA_CURRENT", {'_id': id}):
        result.append(x)
    print(result)
    return jsonify(result)


@app.route('/deviceDataHistory/<deviceId>', methods=['POST'])
def deviceDataHistoryPost(deviceId):
    st = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    mongotime = datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
    jsondata = request.json
    print(jsondata)
    jsondata['timestap'] = mongotime
    print(jsondata)

    condition = {'_id': deviceId}
    jData = {"$set": jsondata}
    dbtb = deviceId + "_DATA"
    db.insert_one(dbtb, jsondata)
    return jsonify()


@app.route('/deviceDataHistory', methods=['GET', 'POST'])
def deviceDataHistory():
    if request.method == 'GET':

        deviceId = request.args.get('deviceId')
        starttime = request.args.get('startTime')
        endtime = request.args.get('endTime')
        print('starttime:%s' % starttime)
        print('endtime:%s' % endtime)

        stime = (datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S"))
        etime = (datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S"))
        dbName = deviceId + '_DATA'

        result = []
        for x in db.find(dbName, {"timestap": {'$gte': stime}, "timestap": {'$lte': etime}}).sort([('timestap', 1)]):
            result.append(x)
        print(result)
        return json.dumps(result, cls=ComplexEncoder)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # 间隔60秒钟执行一次
    scheduler.add_job(tick, 'interval', seconds=60)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)
