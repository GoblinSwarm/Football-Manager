"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import csv

# Importaciones del modelo
from api.models import db, User, Region, Position, Position_Player, Player, Team, Stadium, Trainer, Trainer_Type, League, Match


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

@api.route('/region', methods=['GET'])
def get_region():
    region = Region.query.all
    return jsonify([item.serialize() for item in region]), 200

@api.route('/position', methods=['GET'])
def get_position():
    position = Position.query.all
    return jsonify([item.serialize() for item in position]), 200

@api.route('/player', methods=['GET'])
def get_player():
    player = Player.query.all
    return jsonify([item.serialize() for item in player]), 200

@api.route('/player/<int:theid>', methods=['GET'])
def get_player_position(theid):
    position_player = Position_Player.query.filter_by(player_id=theid).all()

    if position_player is not None:
        return jsonify([item.serialize() for item in position_player]), 200
    else:
        return jsonify("Player or position player are missing"), 400
    
@api.route('/user/<int:theid>', methods=['GET'])
def get_user(theid):
    user = User.query.get(theid)
    return jsonify([item.serialize() for item in user]), 200

@api.route('/team/<int:theid>', methods=['GET'])
def get_team(theid):
    team = Team.query.get(theid)
    return jsonify([item.serialize() for item in team]), 200

@api.route('/team/stadium/<int:theid>', methods=['GET'])
def get_stadium(theid):
    team = Team.query.get(theid)
    if team is not None:
        stadium = Stadium.query.get(team.stadium_id)
        if stadium is not None:
            return jsonify([item.serialize() for item in stadium]), 200
        else:
            return jsonify("Stadium doesnt existe, it has been demolished apparently!"), 400
    else:
        return jsonify("Team couldnt be found!"), 400

@api.route('/team/trainer/<int:theid>', methods=['GET'])
def get_trainer(theid):
    trainer = Trainer.query.get(theid)
    return jsonify([item.serialize() for item in trainer]), 200

@api.route('/trainer_type', methods=['GET'])
def get_trainter_type():
    trainer_type = Trainer_Type.query.all()
    return jsonify([item.serialize() for item in trainer_type])

@api.route('/matches', methods=['GET'])
def get_all_matches():
    all_matches = Match.query.all()
    return jsonify([item.serialize() for item in all_matches]), 200

@api.route('/match/<int:theid>', methods=['GET'])
def get_one_match(theid):
    the_match = Match.query.get(theid)
    return jsonify([item.serialize() for item in the_match]), 200

@api.route('/league/<int:theid>/matches', methods=['GET'])
def get_league_matches(theid):
    match = Match.query.filter_by(league_id=theid).all()
    return jsonify([item.serialize() for item in match]), 200

@api.route('/league/<int:theid>', methods=['GET'])
def get_league(theid):
    league = League.query.get(theid)
    return jsonify([item.serialize() for item in league]), 200

@api.route('/populate_all', methods=['GET'])
def populate():
    #trainer_type - trainer - region - position - stadium - league - team - player - position_player -  match - user
    results=populate_trainer_type()

    return jsonify(results), 200

def populate_trainer_type():
    #trainer_type_id, name, attribute_increase, increase_amount
    csv_to_read = "trainer_type"
    res=read_csv(csv_to_read)
    print(res)

    return res

def read_csv(to_read):
    csvread=[]
    with open(f'/csv/{to_read}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csvread.append(row)

    return csvread