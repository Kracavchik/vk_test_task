from flask import Flask, request, json, jsonify

from json_schemes.contacts_schema import contacts_schema
from utils.json_validator import JsonValidator
from utils.context import context
from utils.config import Config

app = Flask(__name__)
context.app = app


@app.route('/', methods=['GET'])
def index() -> json:
    """
    Base welcome endpoint
    :return: json
    """
    return jsonify({"message": "Welcome to contacts API!"})


@app.route('/api/contacts', methods=['POST'])
@JsonValidator(contacts_schema)
def add_contact() -> json:
    """
    Add new contact in DB
    :return: json
    """
    new_contact = request.get_json()
    new_contact_id = context.db.create_contact(new_contact)
    return jsonify({"Message": f"New contact with id - {new_contact_id} was created"})


@app.route('/api/contacts', methods=['GET'])
def get_contacts() -> json:
    """
    Return list of all contacts from DB
    :return: json
    """
    contacts = context.db.get_contacts()
    return jsonify(contacts)


@app.route('/api/contact', methods=['GET'])
def get_contact() -> json:
    """
    Get single contact by contact_id
    :return: json
    """
    contact_id = request.args.get('contact_id')
    contact_data = context.db.get_contact(contact_id)
    return jsonify(contact_data)


@app.route('/api/contact', methods=['DELETE'])
def delete_contact() -> json:
    """
    Delete single contact by contact_id
    :return: json
    """
    contact_id = request.args.get('contact_id')
    if not contact_id:
        return jsonify({"Error": f"Invalid contact_id"})
    message = context.db.delete_contact(contact_id)
    if message:
        return jsonify(message)
    return jsonify({"Message": f"Contact with id - {contact_id} was deleted"})


@app.route('/api/contact', methods=['PUT'])
@JsonValidator(contacts_schema)
def update_contact() -> json:
    """
    Update single contact fields by contact_id
    :return: json
    """
    contact_id = request.args.get('contact_id')
    updated_fields = request.get_json()
    context.db.update_contact(contact_id, updated_fields)
    return jsonify({"Message": f"Contact with id - {contact_id} was updated"})


def run_api():
    app.run(host=Config.HOSTNAME,
            port=Config.PORT)
