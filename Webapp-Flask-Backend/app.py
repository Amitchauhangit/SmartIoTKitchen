from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from azure.storage.blob import ContainerSasPermissions, generate_container_sas
from pymongo import MongoClient
import secrets
import os

from backend_secrets import get_secrets

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)

CORS(app, origins=os.environ['CORS_URL'], supports_credentials=True) # for API Calls from React app
storage_cred= get_secrets()

AZURE_COSMOSDB_CONNECTION_STRING = storage_cred['cosmosdb_connection_string']
AZURE_ACC_NAME=storage_cred['storage_account_name']
AZURE_PRIMARY_KEY=storage_cred['storage_account_key']
AZURE_CONTAINER = storage_cred['storage_container_name']


AZURE_COSMOSDB_LOGIN_DATABASE_NAME = os.environ['LoginDB']
AZURE_COSMOSDB_IMAGE_DATABASE_NAME = os.environ['ProjectDB']

login_client = MongoClient(AZURE_COSMOSDB_CONNECTION_STRING)
image_client = MongoClient(AZURE_COSMOSDB_CONNECTION_STRING)

login_db = login_client[AZURE_COSMOSDB_LOGIN_DATABASE_NAME]
image_db = image_client[AZURE_COSMOSDB_IMAGE_DATABASE_NAME]



def is_authenticated(username, password):
    
    credentials_collection = login_db['credentials']
    user = credentials_collection.find_one({'username': username, 'password': password})
    
    if user:
        return True
    return False

def generate_sas_token():
    sas = generate_container_sas(account_name=AZURE_ACC_NAME,
                            account_key=AZURE_PRIMARY_KEY,
                            container_name=AZURE_CONTAINER,
                            permission=ContainerSasPermissions(read=True,write=True),
                            expiry=datetime.utcnow() + timedelta(minutes=15))
    
    return sas


def read_data(username):
   
    image_collection = image_db[username]
    data = image_collection.find({}, {'_id': 0})
    image_list = []
    sas_token = generate_sas_token()
    for item in data:
        auth_image_url = item['image_url'] + "?" + sas_token
        image_list.append({
            'auth_image_url': auth_image_url,
            'id': item['id'],
            'image_url': item['image_url']
        })
    return image_list


def write_data(username, data):
    image_collection = image_db[username]
    image_collection.delete_many({})
    image_collection.insert_many(data)

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    credentials_collection = login_db['credentials']
    if credentials_collection.find_one({'username': username}):
        return jsonify({'success': False, 'message': 'Username already exists'})

    user = {'username': username, 'password': password}
    credentials_collection.insert_one(user)

    token = create_access_token(identity=username)
    
    return jsonify({'success': True, 'username': username, 'access_token': token})


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if is_authenticated(username, password):
        token = create_access_token(identity=username)
        return jsonify({'success': True, 'username': username, 'access_token': token})
    else:
       return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/index', methods=['GET','POST'])
@jwt_required()
def index():
    
    current_user = get_jwt_identity()
    data = read_data(current_user)
    return jsonify(data)


@app.route('/add', methods=['POST'])
def add():
    username = request.json['username']
    image_url = request.json['image_url']
    user_details = request.json['user_details']
    
    image_collection = image_db[username]
    new_item = {'id': user_details, 'image_url': image_url}
    result = image_collection.insert_one(new_item)
    inserted_id = str(result.inserted_id)  
    return jsonify({'message': 'Document inserted', 'id': inserted_id}), 201


@app.route('/remove', methods=['POST'])
@jwt_required()
def remove():
    current_user = get_jwt_identity()
    image_url = request.json['image_url']
    image_collection = image_db[current_user]
    result = image_collection.delete_many({'image_url': image_url})
    
    return jsonify({'success': True})
    

@app.route('/logout',methods=['POST'])
def logout():
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()
