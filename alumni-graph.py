import os
from os.path import isfile, join
from flask import Flask, g, request, render_template, Response
from flask.json import jsonify
from datetime import datetime



#
# Constants & initialization
#


app = Flask(__name__)
app.static_url_path = '/static'


"""
# 
# Database manipulation functions
# - connect to the database file
# - query the database
#

def connect_db(db_name):
	db_path = os.path.join(DATABASES_FOLDER, db_name)
	return sqlite3.connect(db_path)

def get_db(db_name):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(db_name)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(db_name, query, args=()):
    cur = get_db(db_name).execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv
"""




#
# Simple error message
#

def make_error(status_code, sub_code, message):
    response = jsonify({
        'status': status_code,
        'sub_code': sub_code,
        'message': message
    })
    response.status_code = status_code
    return response





@app.route('/')
def main():
	"""
	Main app
	"""
	return render_template('tc_alumni.html')




@app.route('/database/', methods=['GET', 'POST'])
def databases():
	"""
	STEP 1
    > list all databases
    > upload a new database
    """
	if request.method == 'POST':
		new_db = request.files['db']
		if new_db and allowed_file(new_db.filename):
			if check_db_exists(new_db.filename):
				return make_error(400, 1, 'database filename already exists')
			new_db.save(os.path.join(app.config['DATABASES_FOLDER'], secure_filename(new_db.filename)))
			key = len(databases_list)
			databases_list.append(new_db.filename)
			return jsonify({'databases': get_db_list()})
		else:
			return make_error(400, 1, 'extension error: only accept .db, .csv and .txt')

    # request.method == 'GET'
	return jsonify({'databases': get_db_list()})





if __name__ == '__main__':
    app.run(debug=True)