import traceback
from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import User,Users
from resources.account import Account,Accounts
import pymysql
import traceback
import jwt
import time
from server import app

#app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == 'NotFound':
        status_code = 404
    elif type(error).__name__ == 'TypeError':
        status_code = 500

    return jsonify({'msg': type(error).__name__}), status_code    

# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     valid_token = jwt.encode({'user_id': user_id, "timestamp": int(time.time())}, 'password', algorithm='HS256').decode('utf-8')
#     print(valid_token)
#     if token == valid_token:
#         pass
#     else:
#         return {'msg': 'Invalid token'}



@app.route('/')
def index():
    return "HAHA:"+'20220408'

@app.route('/user/<user_id>/account/<id>/deposit', methods = ['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    deposit_amount = int(request.get_json()['deposit_amount'])
    old_balance = account['balance']
    new_balance = old_balance + deposit_amount

    sql = 'UPDATE api.accounts SET balance = {} WHERE id = {} AND deleted IS NOT TRUE '.format(new_balance, id)
    response = {}

    try:
        cursor.execute(sql)
        response['msg'] = 'success'             
    except:
        traceback.print_exc()
        response['msg'] = 'failure'

    db.commit()
    db.close()

    return jsonify(response) 

@app.route('/user/<user_id>/account/<id>/withdraw', methods = ['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    withdraw_amount = int(request.get_json()['withdraw_amount'])
    old_balance = account['balance']
    new_balance = old_balance - withdraw_amount

    response = {}
    if new_balance <0:
        response['msg'] = 'Not enough'
        return jsonify(response)    

    sql = 'UPDATE api.accounts SET balance = {} WHERE id = {} AND deleted IS NOT TRUE '.format(new_balance, id)
    
    try:
        cursor.execute(sql)
        response['msg'] = 'success'             
    except:
        traceback.print_exc()
        response['msg'] = 'failure'

    db.commit()
    db.close()

    return jsonify(response) 

def get_account(id):    
    db = pymysql.connect(host='localhost', user='root', password='sarah220', database='api')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """SELECT * FROM accounts WHERE id = '{}' AND deleted IS NOT TRUE """.format(id)
    cursor.execute(sql)
    db.commit()
    account = cursor.fetchone()    
    return db, cursor, account


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)