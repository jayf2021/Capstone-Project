from flask import Flask, request, jsonify, make_response, session

from config import app, db

from models import db, User, Brewery, Review, Favorite


app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/signupuser', methods=['POST'])
def signup_user():
    request_json = request.get_json()
    
        
    name = request_json.get('name')
    email = request_json.get('email')
    new_user = User(
        name = name,
        email = email,
        )

    password = request_json.get('password')
    new_user.password_hash = password
    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id
    session['user_type'] = 'user'
    
    return new_user.to_dict()

@app.route('/check_session', methods=['GET'])
def check_session():
    # user = None
    if session.get('user_id'):
        if session.get('user_type') == 'user':
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200

    return {'error': '401 Unauthorized'}, 401

@app.route('/login', methods=['POST'])
def login():
    request_json = request.get_json()
    email = request_json.get('email')
    password = request_json.get('password')
    check_for_influencer_account = User.query.filter(User.email == email).first()

@app.route('/logout', methods=['DELETE'])
def logout():
    
    if session.get('user_id'):
        session['user_id'] = None
        return {}, 204
    return {'error': '401 Unauthorized'}, 401

@app.route('/users', methods=['GET', 'POST'])
def user_index():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([i.to_dict() for i in users])
    elif request.method == 'POST':
        new_user = User(**request.json)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    
@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def users_show(id):
    user = User.query.get(id)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return make_response('', 204)
    
@app.route('/breweries', methods=['GET', 'POST'])
def breweries_index():
    if request.method == 'GET':
        brewery = Brewery.query.all()
        return jsonify([c.to_dict() for c in brewery])
    elif request.method == 'POST':
        new_brewery = Brewery(**request.json)
        db.session.add(new_brewery)
        db.session.commit()
        return jsonify(new_brewery.to_dict()), 201
    
@app.route('/breweries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def breweries_show(id):
    brewery = Brewery.query.get(id)
    if request.method == 'GET':
        return jsonify(brewery.to_dict())
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(brewery, key, value)
        db.session.commit()
        return jsonify(brewery.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(brewery)
        db.session.commit()
        return make_response('', 204)




if __name__ == '__main__':
    app.run(port=5555)
