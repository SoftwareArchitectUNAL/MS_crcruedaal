#!flask/bin/python
from flask import make_response
from flask import Flask, jsonify
from flask import abort
from utils import *
from bson import BSON
from bson import json_util
from flask import request
import json

def init():
	global client_mongo
	global port
	port = 4000
	client_mongo = get_mongo_instance()

app = Flask(__name__)

#--------------------------------Violence events ------------------------------------------

@app.route('/analysis_data/violence_events/', methods=['GET'])
def get_violence_events():
	violence_events = client_mongo.analysis_data.violence_events.find()
	doc = []
	for i in violence_events:
		doc.append(i)
	return json.dumps(doc, sort_keys=True, indent=4, default=json_util.default)

@app.route('/analysis_data/violence_events/<int:event_id>', methods=['GET','PUT','DELETE'])
def get_violence_event(event_id):
	if request.method == 'GET':
		try:
			violence_event=client_mongo.analysis_data.violence_events.find({"_id":event_id})
		except:
			print ("id {} not founded".format(event_id))
			abort(404)
			return 400
		return json.dumps(violence_event[0], sort_keys=True, indent=4, default=json_util.default)
	elif request.method == 'PUT':
	    data = {
			"_id": event_id,
			"vio_type":request.json["vio_type"],
			"vio_place": request.json["vio_place"],
			"vio_victime_id": request.json["vio_victime_id"]
	    	}
	    client_mongo.analysis_data.violence_events.update({"_id":event_id},{ "vio_victime_id" : data["vio_victime_id"], \
		 "vio_place" : data["vio_place"],\
		 "vio_type" : data["vio_type"] })
	    return jsonify({'data': data}),201
	else:
		client_mongo.analysis_data.violence_events.remove({"_id":event_id})
		return "event {} succesfully deleted".format(event_id),201 
#http://0.0.0.0:5000/analysis_data/violence_events/
@app.route('/analysis_data/violence_events/', methods=['POST'])

def create_violence_event():
	print ("-- Request:")
	print request.json
	if not request.json or not "_id" in request.json:
		print ("-- Request:")
		print request.json
		abort(400)
	data = {
		"_id": request.json["_id"],
		"vio_type":request.json["vio_type"],
		"vio_place": request.json["vio_place"],
		"vio_victime_id": request.json["vio_victime_id"]
    	}
	client_mongo.analysis_data.violence_events.insert(data)
	return jsonify({'data': data}),201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	init()
	app.run(debug=True,host='0.0.0.0',port=port)
