from flask import Blueprint, redirect, render_template, request, jsonify
from . import db
from flask_login import login_required, current_user
from flask_cors import CORS
import uuid

main = Blueprint('main', __name__)

CORS(main, resources={r"/*": {'origins': "*"}})


@main.route('/')
def index():
    return render_template('index.html')


cards = []


@main.route('/cards', methods=['GET'])
@login_required
def loadCardPage():
    return render_template('cards.html', name=current_user.name)


@main.route('/getcards', methods=['GET'])
def all_cards():
    response_object = {'status': 'success'}
    if request.method == "GET":
        response_object['cards'] = cards
        return jsonify(response_object)


@main.route('/cards', methods=['POST'])
def add_cards():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        cards.append({
            'id': uuid.uuid4().hex,
            'front': post_data.get('front'),
            'back': post_data.get('back'),
            'flipped': "false"
        })
        response_object['message'] = 'Card Added!'
    return jsonify(response_object)


@main.route('/cards/<card_id>', methods=['PUT', 'DELETE'])
def single_card(card_id):
    response_object={'status':'success'}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_card(card_id)
        cards.append({
            'id': uuid.uuid4().hex,
            'front':post_data.get('front'),
            'back': post_data.get('back'),
            'flipped': "false"
        })
        response_object['message'] = "Card Updated"
    if request.method == "DELETE":
        remove_card(card_id)
        response_object['message'] = "Card Deleted"
    return jsonify(response_object)

def remove_card(card_id):
    for card in cards:
        if card['id']==card_id:
            cards.remove(card)
            return True
    return False
        
