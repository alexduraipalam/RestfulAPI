from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
import sys

mysql = MySQL()
app = Flask(__name__)

port = 4003
env = "test"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        env = sys.argv[1]
        print("env=" + env)
    if len(sys.argv) > 2:
        port = sys.argv[2]
        print("port=" + port)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'welcome1'
app.config['MYSQL_DATABASE_DB'] = env
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)


class Department(Resource):
    def get(self, dept_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        if dept_id > 0:
            select_query = "select * from departments where  dept_id = " + str(dept_id)
        else:
            select_query = "select max(dept_id) from departments"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            resp = jsonify(rows)
            return resp

        return {'department': None}, 404

    def post(self, dept_id):
        data = request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_query = "insert into departments (dept_id, dept_name) values (" + \
                       str(dept_id) + ", '" + data['dept_name'] + "')"
        cursor.execute(insert_query)
        conn.commit()
        conn.close()
        department = {'dept_id': dept_id, 'dept_name': data['dept_name']}
        return department, 201


class Departments(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        select_query = "select * from departments"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            resp = jsonify(rows)
            return resp

        return {'departments': None}, 404


api.add_resource(Department, '/department/<int:dept_id>')
api.add_resource(Departments, '/departments')

app.run(port=port)
