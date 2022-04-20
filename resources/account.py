from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')


class Account(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='sarah220', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, user_id, id):
        db, cursor = self.db_init()
        sql = """SELECT * FROM api.accounts WHERE id = '{}' AND deleted IS NOT TRUE """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()
        return jsonify({'data': user})

    def patch(self, user_id, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']            
        }
        
        query = []

        for key, value in account.items():
            if value is not None:
                query.append(key + " = '{}' ".format(value))
        
        query = ", ".join(query)

        sql = "UPDATE api.accounts SET {} WHERE id = '{}' ".format(query, id)

        response = {}

        try:
            cursor.execute(sql)
            response['msg'] = 'success'
            db.commit()            

        except:
            traceback.print_exc()
            response['msg'] = 'failure'

        db.close()

        return jsonify(response) 

    def delete(self, user_id, id):
        db, cursor = self.db_init()
        sql = """UPDATE api.accounts SET deleted = true WHERE id = '{}' """.format(id)

        response = {}

        try:
            cursor.execute(sql)
            response['msg'] = 'success'
            db.commit()            

        except:
            traceback.print_exc()
            response['msg'] = 'failure'

        db.close()

        return jsonify(response)


class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='sarah220', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        return db, cursor

    def get(self, user_id):
        db, cursor = self.db_init()            
        
        sql = 'SELECT * FROM api.accounts WHERE deleted IS NOT TRUE AND user_id = "{}" '.format(user_id)
        
        print(sql)
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()

        return jsonify({'data': users})

    def post(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']            
        }

        sql = """
            INSERT INTO api.accounts(balance,account_number,user_id) VALUES('{}','{}','{}')
        """.format(account['balance'],account['account_number'],account['user_id'])

        response = {}

        try:
            cursor.execute(sql)
            response['msg'] = 'success'
            db.commit()            

        except:
            traceback.print_exc()
            response['msg'] = 'failure'

        db.close()

        return jsonify(response)