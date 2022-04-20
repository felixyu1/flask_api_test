from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
import traceback


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class Users(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='sarah220', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        return db, cursor

    def get(self):
        db, cursor = self.db_init()
        print(reqparse.request.headers.get("Content-Type"))
        arg = parser.parse_args()              

        sql = 'SELECT * FROM api.users WHERE deleted IS NOT TRUE '
        if arg['gender'] != None:
            sql += ' AND gender = "{}"'.format(arg['gender'])

        print(sql)
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()

        return jsonify({'data': users})

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note']
        }

        sql = """
            INSERT INTO api.users(name,gender,birth,note) VALUES('{}','{}','{}','{}')
        """.format(user['name'],user['gender'],user['birth'],user['note'])

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

