from flask import Flask
#from flask_cors import CORS, cross_origin
from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017/")

def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease
            db.insert({
                "email": "eric.strom@google.com",
                "id": 33,
                "name": "Eric stromberg",
                "password": "eric@123",
                "username": "eric.strom"
            })
            db_tweets.insert({
                "body": "New blog post, Launch your app with the AWS StartupKit!  # AWS",
                "id": 18,
                "timestamp": "2017-03-11T06:39:40Z",
                "tweetedby": "eric.strom"
            })
            db_api.insert({
                "buildtime": "2017-01-01 10:00:00",
                "links": "/api/v1/users",
                "methods": "get, post, put, delete",
                "version": "v1"
            })
            db_api.insert({
                "buildtime": "2017-02-11 10:00:00",
                "links": "api/v2/tweets",
                "methods": "get, post",
                "version": "2017-01-10 10:00:00"
            })
            print("Database Initialize completed!")
        else:
            print("Database already Initialized!")
    except:
        print(" Database creation failed!!")

app = Flask(__name__)
#app.config['SERVER_NAME'] = 'enrg_sy:5000'
#app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KTq'

#CORS(app)

from flask import jsonify
import json
import sqlite3

from flask import make_response


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found1!'}), 404)


@app.route("/performance")
def get_perf_counter():

    strCount1 = "<div style=""position:relative;width:100%;height:60%"">" \
        "<iframe width=""384"" height=""216""" \
        " src=""https://insights-embed.newrelic.com/embedded_widget/y8OoxNBFXRR6yDOsQCIDGPlTkEA6LnJi"" frameborder=""0""" \
        " style=""position:absolute;width:100%;height:100%""></iframe></div>" \
        "<div id = ""we"" style=""position:relative;width:100%;height:60%"">" \
        " <iframe width=""384"" height=""216"" " \
        " src=""https://insights-embed.newrelic.com/embedded_widget/35HhAcTJ1y3KgDpbnSDmcI8y_5R01b1n"" frameborder=""0""" \
        " style=""position:absolute;width:100%;height:100%""></iframe></div>"

    return strCount1


@app.route("/api/v1/info")
def home_index():
    api_list = []
    db = connection.cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version': api_list}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


def list_users():
    api_list=[]
    db = connection.cloud_native.users
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'user_list': api_list})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

def list_user(user_id):
    api_list=[]
    db = connection.cloud_native.users
    for i in db.find({'id':user_id}):
        api_list.append(str(i))
    
    if api_list == []:
        abort(404)

    return jsonify({'user_details':api_list})

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request1'}), 400)


@app.errorhandler(401)
def invalid_request1(error):
    return make_response(jsonify({'error': 'Bad Request2'}), 400)


@app.errorhandler(405)
def invalid_request2(error):
     return make_response(jsonify({'error': 'Bad Request5'}), 400)


@app.errorhandler(403)
def invalid_request3(error):
    return make_response(jsonify({'error': 'Bad Request4'}), 400)


from flask import request, abort

import random

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not \
        'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json['name'],
        'password': request.json['password'],
        'id': random.randint(1, 1000)
    }
    return jsonify({'status': add_user(user)}), 201


def add_user(new_user):
    api_list=[]
    print(new_user)
    db = connection.cloud_native.users
    user = db.find({'$or':[{"username":new_user['username']}, {"email":new_user['email']}]})
    for i in user:
        print(str(i))
        api_list.append(str(i))

    if api_list == []:
        db.insert(new_user)
        return "Succes"
    else:
        abort(409)


@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = request.json['username']
    return jsonify({'status': del_user(user)}), 200


def del_user(del_user):
    db = connection.cloud_native.users
    api_list = []
    for i in db.find({'username':del_user}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
        db.remove({'username':del_user})
        return "Succes"

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    print(user_id)
    user = {}
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    return jsonify({'status': upd_user(user)}), 200

def upd_user(user):
    api_list=[]
    print(user)
    db_user = connection.cloud_native.users
    users = db_user.find_one({"id":user['id']})
    for i in users:
        api_list.append(str(i))
    if api_list == []:
        abort(409)
    else:
        db_user.update({'id':user['id']},{'$set': user},upsert=False)
        return "Succes"


@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()


def list_tweets():
    api_list = []
    db = connection.cloud_native.tweets
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'tweets_list': api_list})

import time


@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'Body' in request.json:
        abort(400)
    user_tweet['id'] = request.json['id']
    user_tweet['tweetedby'] = request.json['username']
    user_tweet['body'] = request.json['Body']
    user_tweet['created_at'] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(user_tweet)
    return add_tweet(user_tweet)


def add_tweet(new_tweets):
    api_list = []
    db_users = connection.cloud_native.users
    db_tweets = connection.cloud_native.tweets
    print(new_tweets)
    users = db_users.find({"username":new_tweets['tweetedby']})
    for user in users:
        api_list.append(str(user))
    if api_list == []:
        abort(400)
    else:
        db_tweets.insert(new_tweets)
        return "Succes"

#sdfsd

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)


def list_tweet(user_id):
    db = connection.cloud_native.tweets
    api_list = []
    tweets = db.find({'id':user_id})
    for tweet in tweets:
        api_list.append(str(tweet))
    if api_list == []:
        abort(404)
    else:
        return jsonify({"tweet":api_list})


from flask import render_template, make_response, url_for, request, redirect, session


def sumSessionCounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


@app.route('/')
def main():
    sumSessionCounter()
    return render_template('main.html')


@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        # And then redirect the user to the main page
        return redirect(url_for('main'))
    else:
        return render_template('addname.html', session=session)


@app.route('/adduser')
def adduser():
    return render_template('adduser.htm')


@app.route('/addtweets')
def addtweets():
    return render_template('addtweets.htm')


@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('main'))


@app.route('/set_cookie')
def cookie_insertion():
    redirect_to_main = redirect('/')
    response = app.make_response(redirect_to_main)
    response.set_cookie('cookie_name2', value='qwqwqw')
    return response

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    create_mongodatabase()
    app.run(host='0.0.0.0', port=5000, debug=True)
