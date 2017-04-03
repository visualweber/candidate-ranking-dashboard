import json
import itertools
from flask import request as req
from flask.ext.mysql import MySQL
from flask import Flask, render_template, jsonify
from utils.search_candidate import find_candidate_by_skill
from utils.word2vec_model import *

# Init app
app = Flask(__name__)
app.debug = True
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


def dictfetchall(cursor):
    desc = cursor.description
    return dict(itertools.izip([col[0] for col in desc], cursor.fetchone()))

def dictfetchall_aslist(cursor):
    desc = cursor.description
    return [ dict(itertools.izip([col[0] for col in desc], row)) for row in cursor.fetchall() ] 

@app.route("/api/v1/candidate/<int:candidate_id>")
def api_candidate(candidate_id):
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM candidates
		JOIN c_details ON candidates.candidate_id = c_details.c_details_candidate_id
		JOIN c_employment ON candidates.candidate_id = c_employment.c_employment_candidate_id
		WHERE candidate_id = %s """, (candidate_id, ))
	result = dictfetchall(cursor)
	# cursor.close()
	# conn.close()

	return jsonify(result)
	# return app.response_class(
	# 	response=json.dumps(result),
	# 	status=200,
	# 	mimetype='application/json'
	# )


@app.route("/api/v1/matching_candidates")
def matching_candidates():
	limit = max(min(req.args.get('limit', default=10, type=int), 100), 5)
	skills = req.args.get('skills', type=str)
	if not skills: return []
	skills = str(skills).split(',')
	
	list_candidates = find_candidate_by_skill(skills, limit=limit)
	_ids = [ str(c['candidate_id']) for c in list_candidates ]

	cursor = conn.cursor()
	cursor.execute("""
		SELECT c.*, GROUP_CONCAT(DISTINCT skill.name SEPARATOR ', ') as skills 
		FROM candidates c join c_skill_tags skill on c.candidate_id = skill.candidate_id 
		WHERE c.candidate_id IN (%s)
		group by c.candidate_id 
		limit 10
		""" % (', '.join(_ids)) )
	# results = cursor.fetchall()
	results = dictfetchall_aslist(cursor)

	for i in results:
		for c in list_candidates:
			if c['candidate_id'] == i['candidate_id']:
				i['matching_score'] = c['score']
				del c
	
	return app.response_class(
		response=json.dumps(results),
		status=200,
		mimetype='application/json'
	)


@app.route("/api/v1/candidates")
def api_candidates():
	limit = max(req.args.get('limit', default=10, type=int), 100)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM candidates LIMIT %s", (limit, ))
	results = cursor.fetchall()
	cursor.close()
	conn.close()
	
	
	return app.response_class(
		response=json.dumps(results),
		status=200,
		mimetype='application/json'
	)


@app.route("/api/v1/relevant_skills")
def relevant_skills():
	skills = req.args.get('skills', default='', type=str)
	if not skills: return []
	skills = str(skills).split(',')

	relevant_skills = [ { 'name': skill, 'data': get_relevant_skill(skill) }  for skill in skills ]
	return app.response_class(
		response=json.dumps(relevant_skills),
		status=200,
		mimetype='application/json'
	)

@app.route("/api/v1/skill")
def api_skill():
	# Data source
	data_source = req.args.get('source', default='candidate', type=str)
	
	# Candidate id or cv id
	_id = req.args.get('id', default=0, type=int)

	if data_source == 'candidate':
		cursor = conn.cursor()
		cursor.execute("SELECT name FROM c_skill_tags WHERE type = 'skill' AND candidate_id = %s", (_id, ))
		results = cursor.fetchall()
		if results: results = [ result[0] for result in results ]

	# Data CV
	else:
		cursor = conn.cursor()
		cursor.execute("SELECT job_keywords FROM jobs WHERE job_id = %s LIMIT 1", (_id, ))
		results = cursor.fetchall()
		if results: results = results[0]
		if results: results = results[0]
		if results: results = results.split(',')
		if results: results = [ result.strip() for result in results ]
	cursor.close()
	conn.close()
	
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
#	 return 'Database connection failed', 500

if __name__ == "__main__":
	app.run()
