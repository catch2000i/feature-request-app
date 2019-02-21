#!flask/bin/python3.6

from threading import Lock
import random
import datetime
import collections

from flask import Flask, jsonify, abort, make_response, request, url_for, json, render_template, send_from_directory

from sqlalchemy import create_engine, func, update
from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import DateTime
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy_declarative import Base, Feature, Client, ProductArea
from sqlalchemy.ext.declarative import DeclarativeMeta

lock = Lock()

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine))

#DBSession = sessionmaker(bind=engine)
#session = DBSession()


app = Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/demo.html')
def demo():
	return render_template('demo.html')




# GET ALL FEATURES
# http://127.0.0.1:5000/api/features
@app.route('/api/features', methods=['GET'])
def get_features():
	res = session.query(Feature).all();
	response = construct_json_response(res)
	return response


# GET ALL CLIENTS
# http://127.0.0.1:5000/api/clients
@app.route('/api/clients', methods=['GET'])
def get_clients():
	res = session.query(Client).all();
	response = construct_json_response(res)
	return response


# GET ALL PRODUCTAREAS
# http://127.0.0.1:5000/api/productareas
@app.route('/api/productareas', methods=['GET'])
def get_productareas():
	res = session.query(ProductArea).all();
	response = construct_json_response(res)
	return response



# ADD NEW FEATURE
# http://127.0.0.1:5000/api/add_feature
@app.route('/api/add_feature', methods=['POST', 'GET'])
def add_feature():
	# read from body
	if request.method == 'POST':
		
		result = request.form;
		
		for v in result:
			featureValues = json.loads(v)
		
		client_priority = featureValues.get("client_priority");
		target_date = featureValues.get("target_date");
		client_id=featureValues.get("client_id");
		client_priorities_array = {};
		
		for row in session.query(Feature).filter(Feature.client_id==client_id).all():
			client_priorities_array[row.client_priority] = row.client_priority;
		
		client_priorities_array_sorted = collections.OrderedDict(sorted(client_priorities_array.items()))
		
		build_new_dict = {}
		isFound = False;
		old_value = 0;
		max_key_values = 0;
		
		for key, value in client_priorities_array_sorted.items():
			if str(key) == str(client_priority):
				isFound = True;
				old_value = value - 1;
			if isFound == True:
				if (old_value + 1) == value:
					build_new_dict[key] = value + 1;
					max_key_values = key;
				elif (old_value + 1) < value:
					break;
			old_value = value;
		
		build_new_dict_keys = list(build_new_dict.keys());
		
		# LOCK THREAD
		# TODO: this method works only for single threaded mode of Flask
		# For real production system either db locking or journal should be used
		with lock:
			if isFound == True:
				build_new_dict_keys_length = len(build_new_dict_keys);
				for i in range(build_new_dict_keys_length-1, -1, -1):
					cl_pr = build_new_dict_keys[i];
					upd_cl_pr = cl_pr + 1;
					stmt = update(Feature).where(Feature.client_id==client_id).where(Feature.client_priority==cl_pr).values(client_priority=upd_cl_pr);
					session.execute(stmt);
					session.commit();
			
			d = datetime.datetime.strptime(target_date, '%m/%d/%Y').date();
			new_feature = Feature(title=featureValues.get("title"), description=featureValues.get("description"), client_priority=client_priority, 
				client_id=featureValues.get("client_id"), product_area_id=featureValues.get("product_area_id"), target_date=d)
			session.add(new_feature)
			session.commit()
		# RELEASE THREAD
		
		id = new_feature.id;
		return "{ \"id\":" + str(id) + "}";



# DELETE FEATURE
# http://127.0.0.1:5000/api/delete_feature/1
@app.route('/api/delete_feature/<int:feature_id>', methods=['GET'])
def delete_feature(feature_id):
	session.query(Feature).filter(Feature.id==feature_id).delete()
	session.commit()
	return "{ \"id\":" + str(feature_id) + "}";



@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Not found title'}), 400)


def construct_json_response(res):
	json_res = "["
	for o in res:
		if len(json_res) > 20 :
			json_res+=","
		json_res += json.dumps(o,cls=AlchemyEncoder);

	json_res += "]";
	response = app.response_class(
		response=json_res,
		status=200,
		mimetype='application/json'
	);
	return response;


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
	app.run(host="0.0.0.0")
	app.run(debug=True)


