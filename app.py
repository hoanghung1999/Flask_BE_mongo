from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'demo'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/demo'

mongo = PyMongo(app)

@app.route('/user', methods=['GET'])
def get_all_stars():
  customer = mongo.db.customer
  output = []
  for s in customer.find():
    output.append({'name' : s['name'], 'username' : s['username'],'password':s['password']})
  return jsonify(output)

@app.route('/user/login', methods=['POST'])
def get_one_star():
  customer = mongo.db.customer
  username=request.json['username']
  password=request.json['password']
  s = customer.find_one({'username' :username,'password':password})
  if s:
    output = {'name' : s['name'], 'username' : s['username'],'password':s['password'],'status':'ok'}
  else:
    output = {'status':'Username or password fail'}
  return jsonify(output)

@app.route('/user/creat', methods=['POST'])
def add_user():
  customer = mongo.db.customer
  name = request.json['name']
  username = request.json['username']
  password= request.json['password']
  try:
    star_id = customer.insert({'name': name,'username':username,'password':password})
    customernew = customer.find_one({'_id': star_id })
    output = {'name' : customernew['name'], 'username' : customernew['username'],'password':customernew['password'],'status':'ok'}
  except:
    output={'status':'username exist'}
  return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)

