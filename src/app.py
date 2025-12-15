"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200


@app.route('/members', methods=['POST'])
def create_member():
    body = request.get_json(silent=True)
    print("you added", body)
    if body is None:
        return jsonify({"msg": "you need to send something i this body"}), 400
    if 'first_name' not in body:
        return jsonify({"msg": "this field is required"}), 400
    if 'age' not in body:
        return jsonify({"msg": "this field is required"}), 400
    if 'lucky_numbers' not in body:
        return jsonify({"msg": "this field is required"}), 400
    
    new_member = {
        'first_name': body['first_name'],
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers'],
        'last_name': jackson_family.last_name,
        "id": jackson_family._generate_id()
    }
    print(new_member)

    new_member_added = jackson_family.add_member(new_member)
    return jsonify( new_member_added), 200

@app.route('/members/<int:id>', methods= ['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"msg": "Member not found"}), 404

    return jsonify(member), 200

@app.route('/members/<int:id>', methods = ['DELETE'])
def delete_member(id):
    member_delete = jackson_family.delete_member(id)

    if member_delete:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"done": False}), 400
    
   


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
