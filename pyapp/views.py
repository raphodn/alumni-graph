from pyapp import app
from models import *
from flask import request, session, redirect, jsonify, url_for, abort, render_template, flash
from flask_oauthlib.client import OAuth

oauth = OAuth(app)

"""
linkedin = oauth.remote_app(
    'linkedin',
    consumer_key='k8fhkgkkqzub',
    consumer_secret='ZZtLETQOQYNDjMrz',
    request_token_params={
        'scope': 'r_basicprofile',
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)
"""

empty_values = {None, ''}


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
    return render_template('alumni_graph.html')


"""
ALL DATA
"""
@app.route('/api/all', methods=['GET'])
def get_all():
    return jsonify({'nodes': get_all_nodes(), 'relationships': get_all_relationships()})



"""
PERSON API
"""
@app.route('/api/person', methods=['GET'])
def get_persons():
    """
    search by first_name, last_name, seperate, together ??
    """
    return get_nodes(user)

@app.route('/api/user', methods=['POST'])
def create_user():
    if not request.json or not 'first_name' or not 'last_name' in request.json:
        return make_error(400, 1, 'missing User data. Expecting first_name & last_name fields')
    
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    if not User().create(first_name, last_name):
        return make_error(400, 1, 'error creating User node')

    return jsonify({'task': task}), 201


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return get_node(user_id)




"""
SCHOOL API
"""
@app.route('/api/school', methods=['GET'])
def get_schools():
    school_name = request.args.get('name', None)
    school_search = request.args.get('search', None)

    # get all schools
    if school_name in empty_values:
        return jsonify({'schools': School().get_all_schools()})

    else:
        # get specific school
        if (school_search in empty_values) or (school_search != 'True'):
            return jsonify({'school': School(school_name).get_school()})

        # search schools
        else:
            return jsonify({'schools': School(school_name).search_schools()})


@app.route('/api/school', methods=['POST'])
def create_school():
    if not request.json or not 'name' in request.json:
        return make_error(400, 1, 'missing School data. Expecting name field')
    else:
        name = request.json['name']
        School(name).create()



@app.route('/api/school/<int:school_id>/fields', methods=['GET'])
def get_school_fields(school_id):
    return get_all_fields_from_school(school_id)


"""
FIELD API
"""
@app.route('/api/field', methods=['GET'])
def get_fields():
    return get_nodes(field)


@app.route('/api/field/<int:field_id>', methods=['GET'])
def get_field(field_id):
    return get_node(field_id)



"""
YEAR API
"""
@app.route('/api/year', methods=['GET'])
def get_years():
    return get_nodes(year)


@app.route('/api/year/<int:year_id>', methods=['GET'])
def get_year(year_id):
    return get_node(year_id)




"""
COMPANY API
"""
@app.route('/api/company', methods=['GET'])
def get_companies():
    company_name = request.args.get('name', None)
    company_search = request.args.get('search', None)

    # get all companies
    if company_name in empty_values:
        return jsonify({'companies': Company().get_all_companies()})

    else:
        # get specific company
        if (company_search in empty_values) or (company_search != 'True'):
            return jsonify({'company': Company(company_name).get_company()})

        # search companies
        else:
            return jsonify({'companies': Company(company_name).search_companies()})


@app.route('/api/company', methods=['POST'])
def create_company():
    if not request.json or not 'name' in request.json:
        return make_error(400, 1, 'missing Company data. Expecting name field')
    else:
        name = request.json['name']
        Company.create(name)





"""
POSITION API
"""
@app.route('/api/position', methods=['GET'])
def get_positions():
    return get_nodes(position)


@app.route('/api/position/<int:position_id>', methods=['GET'])
def get_position(position_id):
    return get_node(position_id)










############################################################################################
# from https://github.com/nicolewhite/neo4j-flask
############################################################################################




@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            error = 'Your username must be at least one character.'
        elif len(password) < 5:
            error = 'Your password must be at least 5 characters.'
        elif not User(username).set_password(password).register():
            error = 'A user with that username already exists.'
        else:
            flash('Successfully registered. Please login.')
            return redirect(url_for('login'))

    return render_template('register.html', error=error)




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username)

        if not user.verify_password(password):
            error = 'Invalid login.'
        else:
            session['username'] = user.username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)




@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))





@app.route('/add_post', methods=['POST'])
def add_post():
    user = User(session['username'])
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if title == '':
        abort(400, 'You must give your post a title.')
    if tags == '':
        abort(400, 'You must give your post at least one tag.')
    if text == '':
        abort(400, 'You must give your post a texy body.')

    user.add_post(title, tags, text)
    return redirect(url_for('index'))




@app.route('/like_post/<post_id>', methods=['GET'])
def like_post(post_id):
    username = session.get('username')
    if not username:
        abort(400, 'You must be logged in to like a post.')

    user = User(username)
    user.like_post(post_id)
    flash('Liked post.')
    return redirect(request.referrer)




@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    posts = get_users_recent_posts(username)

    similar = []
    common = []

    viewer_username = session.get('username')
    if viewer_username:
        viewer = User(viewer_username)
        # If they're visiting their own profile, show similar users.
        if viewer.username == username:
            similar = viewer.get_similar_users()
        # If they're visiting another user's profile, show what they
        # have in common with that user.
        else:
            common = viewer.get_commonality_of_user(username)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )