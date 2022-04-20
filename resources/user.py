from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
import traceback
from server import db
from models import UserModel
from dotenv import load_dotenv
import os

load_dotenv()

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')


class User(Resource):
    def db_init(self):
        db = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_SCHEMA'))
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """SELECT * FROM api.users WHERE id = '{}' AND deleted IS NOT TRUE """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()
        return jsonify({'data': user})

    def patch(self, id):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        # user = {
        #     'name': arg['name'],
        #     'gender': arg['gender'],
        #     'birth': arg['birth'],
        #     'note': arg['note']
        # }
        
        user = UserModel.query.filter_by(id=id, deleted=None).first()

        if arg['name'] != None:
            user.name = arg['name']
        if arg['gender'] != None:
            user.gender = arg['gender']
        if arg['birth'] != None:
            user.birth = arg['birth']
        if arg['note'] != None:
            user.note = arg['note']

        # query = []

        # for key, value in user.items():
        #     if value is not None:
        #         query.append(key + " = '{}' ".format(value))
        
        # query = ", ".join(query)

        # sql = "UPDATE api.users SET {} WHERE id = '{}' ".format(query, id)

        response = {}

        try:
            # cursor.execute(sql)
            db.session.commit() 
            response['msg'] = 'success'              
        except:
            traceback.print_exc()
            response['msg'] = 'failure'

        # db.close()

        return jsonify(response) 

    def delete(self, id):
        # db, cursor = self.db_init()
        # sql = """UPDATE api.users SET deleted = true WHERE id = '{}' """.format(id)

        user = UserModel.query.filter_by(id=id, deleted=None).first()
        response = {}

        try:
            # cursor.execute(sql)
            db.session.delete(user)
            db.session.commit()
            response['msg'] = 'success'
            # db.commit()            

        except:
            traceback.print_exc()
            response['msg'] = 'failure'

        # db.close()

        return jsonify(response)


class Users(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='sarah220', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        return db, cursor

    def get(self):
        # db, cursor = self.db_init()            
        # arg = parser.parse_args()

        # sql = 'SELECT * FROM api.users WHERE deleted IS NOT TRUE '
        
        # if arg['gender'] != None:
        #     sql += ' AND gender = "{}" '.format(arg['gender'])

        # print(sql)
        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()

        users = UserModel.query.filter(UserModel.deleted.isnot(True))

        return jsonify({'data': list(map(lambda user: user.serialize(), users))})

    def post(self):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note']
        }

        # sql = """
        #     INSERT INTO api.users(name,gender,birth,note) VALUES('{}','{}','{}','{}')
        # """.format(user['name'],user['gender'],user['birth'],user['note'])
        new_user = UserModel(name=user['name'], gender=user['gender'], birth=user['birth'], note=user['note'])
        
        response = {}
        status_code = 200

        try:
            # cursor.execute(sql)
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'success'
            # db.commit()            

        except:
            traceback.print_exc()
            status_code = 487
            response['msg'] = 'failure'

        # db.close()

        return make_response(jsonify(response), status_code)