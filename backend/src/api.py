import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import NotFound

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    search_term = request.args.get('searchTerm')
    drinks_q = Drink.query
    if search_term:
        drinks_q = drinks_q.filter(Drink.title.ilike(search_term))
    drinks_result = []
    for drink in drinks_q.all():
        drinks_result.append(drink.short())
    return jsonify({"succes": True, "drinks": drinks_result})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@requires_auth('get:drinks-detail')
@app.route('/drinks-detail')
def get_drink_details():
    search_term = request.args.get('searchTerm')
    drinks_q = Drink.query
    if search_term:
        drinks_q = drinks_q.filter(Drink.title.ilike(search_term))
    drinks_result = []
    for drink in drinks_q.all():
        drinks_result.append(drink.long())
    return jsonify({"succes": True, "drinks": drinks_result})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@requires_auth('post:drinks')
@app.route('/drinks', methods=['POST'])
def create_drink():
    data = request.json
    parts = data.get('recipe', [])
    if not parts:
        return bad_request_error('Recipe is needed')
    for part in parts:
        if 'name' not in part:
            return bad_request_error('Name of recipe part must be included')
        if 'parts' not in part:
            return bad_request_error('Number of parts be included in a recipe part')
        if 'color' not in part:
            return bad_request_error('Color of parts be included in a recipe part')
    drink = Drink(title=data.get('title'), recipe=json.dumps(parts))
    db.session.add(drink)
    db.session.commit()
    return jsonify({"success": True, "drinks": [drink.short()]}), 201


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def edit_drink(drink_id):
    pass


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    pass


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(400)
def bad_request_error(error='Bad request'):
    return jsonify({'success': False, 'error': 400, 'message': error}), 400

@app.errorhandler(401)
def not_found_error(error='Unauthorized'):
    if isinstance(error, NotFound):
        return jsonify({'success': False, 'error': 401, 'message': str(error)}), 401
    return jsonify({'success': False, 'error': 401, 'message': error}), 401

@app.errorhandler(403)
def not_found_error(error='Forbidden'):
    if isinstance(error, NotFound):
        return jsonify({'success': False, 'error': 403, 'message': str(error)}), 403
    return jsonify({'success': False, 'error': 403, 'message': error}), 403

@app.errorhandler(404)
def not_found_error(error='Resource not found'):
    if isinstance(error, NotFound):
        return jsonify({'success': False, 'error': 404, 'message': str(error)}), 404
    return jsonify({'success': False, 'error': 404, 'message': error}), 404

@app.errorhandler(500)
def server_error(error='Server Error'):
    return jsonify({'success': False, 'error': 500, 'message': error}), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(auth_error):
    return jsonify({'success': False, 'error': auth_error.status_code, 'message': auth_error.error}), auth_error.status_code