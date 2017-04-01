import json
from flask import request as req
from flask.ext.mysql import MySQL
from flask import Flask, render_template, jsonify
# from werkzeug import generate_password_hash, check_password_hash

# Init app
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'vsource'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/api/v1/candidate")
def api_candidate():
	limit = max(req.args.get('limit', default=10, type=int), 100)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM candidates LIMIT %s", (limit, ))
	results = cursor.fetchall()
	
	return app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

# @app.errorhandler(DatabaseError)
# def special_exception_handler(error):
#     return 'Database connection failed', 500

if __name__ == "__main__":
    app.run()
