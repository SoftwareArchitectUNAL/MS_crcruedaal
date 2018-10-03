#!flask/bin/python
from flask import make_response
from flask import Flask, jsonify
from flask import abort
from utils import *
from bson import BSON
from bson import json_util
import json

def init():
	global client_mongo
	client_mongo = get_mongo_instance()

app = Flask(__name__)

#--------------------------------GET ------------------------------------------

@app.route('/analysis_data/violence_events/', methods=['GET'])
def get_violence_events():
	violence_events = client_mongo.analysis_data.violence_events.find()
	doc = []
	for i in violence_events:
		doc.append(i)
	return json.dumps(doc, sort_keys=True, indent=4, default=json_util.default)

@app.route('/analysis_data/violence_events/<int:event_id>', methods=['GET'])
def get_violence_event(event_id):
	try:
		violence_event=client_mongo.analysis_data.violence_events.find({"_id":event_id})
	except:
		print ("id {} not founded".format(event_id))
		abort(404)
		return 0
	return json.dumps(violence_event[0], sort_keys=True, indent=4, default=json_util.default)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	init()
	app.run(debug=True,host='0.0.0.0')
