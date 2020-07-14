from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
import sys

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'welcome1'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)


class Student(Resource):
    def get(self, student_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        select_query = "select * from students where  student_id = " + str(student_id)
        cursor.execute(select_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            resp = jsonify(rows)
            return resp

        return {'student': None}, 404

    def post(self, student_id):
        data = request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_query = "insert into students (student_id, first_name, last_name )values (" + \
                       str(student_id) + ", '" + data['first_name'] + \
                       "', '" + data['last_name'] + "')"
        cursor.execute(insert_query)
        conn.commit()
        conn.close()
        student = {'student_Id': student_id, 'first_name': data['first_name'], 'last_name': data['last_name']}
        return student, 201

    def put(self, student_id):
        data = request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_query = "update students set dept_id = ( select dept_id from departments where " + \
                       "dept_name = '" + data['dept_name'] + "') where  student_id = " + str(student_id)
        cursor.execute(insert_query)
        conn.commit()
        conn.close()
        student = {'student_Id': student_id, 'first_name': data['first_name'], 'last_name': data['last_name'],
                   'dept_name': data['dept_name']}
        return student, 201


class Students(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        select_query = "select * from students"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            resp = jsonify(rows)
            return resp

        return {'students': None}, 404


api.add_resource(Student, '/student/<int:student_id>')
api.add_resource(Students, '/students')

port = 4001
if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print("port=" + port)

app.run(port=port)
