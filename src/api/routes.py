"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import csv
import random
# Importaciones del modelo
from api.models import db, User, Region, Position, PositionPlayer, Player, Team, Stadium, Trainer, League, Match, TrainerType


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
    trainer_type = TrainerType.query.all()
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

def read_csv(to_read):
    csvread=[]
    address="./src/api/csv/" + to_read + ".csv" 

    with open(address, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csvread.append(row)

    return csvread

@api.route('/populate_all', methods=['GET'])
def populate():
    #trainer_type - trainer - region - position - stadium - league - team - player - position_player -  match - user
    results=[]
    results.append(populate_trainer_type())
    results.append(populate_trainer())
    results.append(populate_stadium())
    results.append(populate_region())
    results.append(populate_position())
    results.append(populate_league())
    results.append(populate_team())
    results.append(populate_player())
    
    #results.append(populate_user())
    #results.append(populate_match())

    return jsonify(results), 200

def populate_trainer_type():
    #name, attribute_increase, increase_amount
    csv_to_read = "trainer_type"
    file_read=read_csv(csv_to_read)
    jump = True
    
    for row in file_read[1:]:

            trainertype = TrainerType(
                name=row[0].strip(),  
                attribute_increase=row[1].strip(),  
                increase_amount= int(row[2].strip())
            )
            db.session.add(trainertype)
    try:
        db.session.commit()
        return "TrainerType added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create trainertypes"}), 400
    
def populate_trainer():
    csv_to_read = "trainer"
    file_read=read_csv(csv_to_read)
    #name, trainertype_id
    for row in file_read[1:]:
            trainer = Trainer(
                name=row[0].strip(),  
                trainertype_id=row[1].strip(),  
            )
            print(f"Adding Trainers: {trainer}") 
            db.session.add(trainer)
    try:
        db.session.commit()
        return "Trainers added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create Trainers"}), 400

def populate_stadium():
    csv_to_read = 'stadium'
    file_read=read_csv(csv_to_read)
    #name, standard_seats, bleacher_seats, premium_seats, club_seats, box_seats
    for row in file_read[1:]:
            stadium = Stadium(
                name=row[0].strip(),  
                standard_seats=row[1].strip(),  
                bleacher_seats=row[2].strip(),
                premium_seats=row[3].strip(),
                club_seats=row[4].strip(),
                box_seats=row[5].strip()
            )
            print(f"Adding Trainers: {stadium}") 
            db.session.add(stadium)
    try:
        db.session.commit()
        return "Stadium added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create Stadium"}), 400     

def populate_region():
    csv_to_read = 'region'
    file_read=read_csv(csv_to_read)
    #name, standard_seats, bleacher_seats, premium_seats, club_seats, box_seats
    for row in file_read[1:]:
            region = Region(
                name=row[0].strip(),  
            )
            print(f"Adding Region: {region}") 
            db.session.add(region)
    try:
        db.session.commit()
        return "Region added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create Region"}), 400     

def populate_position():
    csv_to_read = 'position'
    file_read=read_csv(csv_to_read)
    
    for row in file_read[1:]:
            position = Position(
                name=row[0].strip(),  
            )
            print(f"Adding Region: {position}") 
            db.session.add(position)
    try:
        db.session.commit()
        return "Position added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create Position"}), 400     

def populate_league():
    csv_to_read = 'league'
    file_read=read_csv(csv_to_read)
    #name, league_depth, league_number
    for row in file_read[1:]:
            league = League(
                name=row[0].strip(),  
                league_depth=row[1].strip(),
                league_number=row[2].strip()
            )
            print(f"Adding Region: {league}") 
            db.session.add(league)
    try:
        db.session.commit()
        return "League added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create League"}), 400   

def populate_team():
    # En este metodo debe de venir el region_id para llamar
    csv_to_read = 'team'
    file_read=read_csv(csv_to_read)
    #name, finances, trainer_id, stadium_id, league_id
    for row in file_read[1:]:
            team = Team(
                name=row[0].strip(),  
                finances=row[1].strip(),
                trainer_id=row[2].strip(),
                stadium_id=row[3].strip(),
                league_id=row[4].strip()
            )
            print(f"Adding Region: {team}") 
            db.session.add(team)
    try:
        db.session.commit()
        return "Team added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify({"message": "Couldnt create Team"}), 400   

def populate_player():
    #Este metodo es llamado por populate_team y debe traer team_id y region_id
    #name, age, mentality, speed, passes, shoot, stop_ball, defense, physique, precision, goalkeep, salary, team_id, region_id
    # 9 attributes
    teams = Team.query.all()
    regions = Region.query.all()
    player_to_create = 16
        
    for region in regions:
         for team in teams:
            for meta_player in range(player_to_create):
                list_attributes=[]
                for i in range(9):
                        list_attributes.append(random_generator(1, 6))

                player = Player(
                name = random_name(),
                age = random_generator(18, 30),
                mentality = list_attributes[0],
                speed = list_attributes[1],
                passes = list_attributes[2],
                shoot = list_attributes[3],
                stop_ball = list_attributes[4],
                defense = list_attributes[5],
                physique = list_attributes[6],
                precision = list_attributes[7],
                goalkeep = list_attributes[8],
                salary = calculate_salary_based_attributes(list_attributes),
                team_id = team.team_id,
                region_id = region.region_id
                )
                db.session.add(player)  
    try:
        db.session.commit()
        return "Player added"
    except Exception as e:
        print(e.args)
        db.session.rollback()
    return jsonify({"message": "Couldnt create Player"}), 400  
    
def random_name():
    firstname=read_csv("name")
    lastname=read_csv("lastname")
    
    first_part_name=random_generator(0, len(firstname) - 1)
    last_part_name=random_generator(0, len(lastname) - 1)
    
    first=firstname[first_part_name]
    first = ''.join(first)
    last=lastname[last_part_name]
    last = ''.join(last)
    fullname = first + ' ' + last

    return fullname

def calculate_salary_based_attributes(attributes):
    # attributes * 500, magic number
    base_salary= 0
    for value in attributes:
         base_salary += value * 500
    print(f"Base Salary: " + str(base_salary))
    return base_salary

def random_generator(min, max):
    number = random.randint(min, max) 
    return number