"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import csv, random, os
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from base64 import b64encode
from api.utils import set_password
from sqlalchemy import desc
# Importaciones del modelo
from api.models import db, User, Region, Position, PositionPlayer, Player, Team, Stadium, Trainer, League, Match, TrainerType


api = Blueprint('api', __name__)
get_jwt_identity
# Allow CORS requests to this API
CORS(api)

expires_in_minutes = 10
expires_delta = timedelta(minutes=expires_in_minutes)

def check_password(hash_password, password, salt):
    return check_password_hash(hash_password, f"{password}{salt}")


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
    results.append(populate_match())
    #results.append(populate_user())
    
    return jsonify(results), 200

def populate_trainer_type():
    #name, attribute_increase, increase_amount
    csv_to_read = "trainer_type"
    file_read=read_csv(csv_to_read)
    
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
            for i in range(1,4):
                league = League(
                    name=row[0].strip(),  
                    league_depth=row[1].strip(),
                    league_number=row[2].strip(),
                    region_id=i
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
            for i in range(1,4):
                team = Team(
                    name=row[0].strip(),  
                    finances=row[1].strip(),
                    trainer_id=row[2].strip(),
                    stadium_id=row[3].strip(),
                    league_id=row[4].strip(),
                    is_bot = True,
                    region_id=i
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
                exp_mentality = 0,
                speed = list_attributes[1],
                exp_speed = 0,
                passes = list_attributes[2],
                exp_passes = 0,
                shoot = list_attributes[3],
                exp_shoot = 0,
                stop_ball = list_attributes[4],
                exp_stop_ball = 0,
                defense = list_attributes[5],
                exp_defense = 0,
                physique = list_attributes[6],
                exp_physique = 0,
                precision = list_attributes[7],
                exp_precision = 0,
                goalkeep = list_attributes[8],
                exp_goalkeep = 0,
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
    return base_salary

def random_generator(min, max):
    number = random.randint(min, max) 
    return number

def populate_match():   
    
    leagues = League.query.all()
    for league in leagues:
        calendario_ida, calendario_vuelta = calendar_creation(league.league_id)
        create_matches(calendario_ida, calendario_vuelta, league.league_id)
    
    return "Matches Added"

def create_matches(calendario_ida, calendario_vuelta, league_id):
    match_date = 1 
    matches = []
    #match_date, league_id, home_team_id, away_team_id, home_goals, away_goals, result, played
    for jornada in calendario_ida:
        for home_team, away_team in jornada:
            match = Match(
                match_date = match_date,
                league_id = league_id,
                home_team_id=home_team.team_id,
                away_team_id=away_team.team_id,
                home_goals=0,
                away_goals=0,
                result="-",
                played=False
            )
            db.session.add(match)
        match_date += 1

    for jornada in calendario_vuelta:
        for home_team, away_team in jornada:
            match = Match(
                match_date = match_date,
                league_id = league_id,
                home_team_id=home_team.team_id,
                away_team_id=away_team.team_id,
                home_goals=0,
                away_goals=0,
                result="-",
                played=False
            )
            db.session.add(match)
        match_date += 1
    try:
        db.session.commit()
        return 
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify("Matches not working"), 400

def calendar_creation(league_id):
    teams = Team.query.filter_by(league_id=league_id).all()
    
    n = len(teams)
    calendario_ida = []
    calendario_vuelta = []

    for i in range(n - 1):
        jornada = []
        for j in range(n // 2):
            home_team = teams[j]
            away_team = teams[n - 1 - j]
            jornada.append((home_team, away_team))
        
        calendario_ida.append(jornada)
        calendario_vuelta.append([(away_team, home_team) for home_team, away_team in jornada])
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return calendario_ida, calendario_vuelta

@api.route('/user/register', methods=['POST'])
def register_user():
    data_json = request.json
    #name, birthday, email, password, salt, region
    data = {
        "name": data_json.get("name"),
        "birthday": data_json.get("birthday"),
        "email": data_json.get("email"),
        "password": data_json.get("password"),
        "region_id": data_json.get("region_id")
    }
    
    name=data.get("name")
    birthday=data.get("birthday")
    email=data.get("email")
    password=data.get("password")
    user_region_id=data.get("region_id")
    

    if email is None or password is None:
        return jsonify("Email and Password are needed"), 400
    else: 
        user = User.query.filter_by(email=email).one_or_none()
        if user is not None:
            return jsonify("User exists, please login"), 400
        
        salt = b64encode(os.urandom(32)).decode("utf-8")
        password = set_password(password, salt)
        #Aca se genera un equipo nuevo 
        team=new_team_generator(user_region_id)
        user = User(name=name, birthday=birthday, email=email,password=password, salt=salt, region_id=user_region_id, team_id=team.team_id)
        db.session.add(user)

        try:
            db.session.commit()
            return jsonify({"message": "User created!"}), 201
        except Exception as e:
            print(e.args)
            db.session.rollback
            return jsonify({"Error Message": f"User was not created: {e.args}"}), 400
        
def new_team_generator(user_region_id):
    team_found = False
    while team_found == False:
        region_leagues = League.query.filter_by(region_id=user_region_id)
        print(region_leagues)
        for league in region_leagues:
            if league is not None:
                team = Team.query.filter_by(is_bot=True).first()
                return team
            else:
                generate_bot_leagues(user_region_id)
                generate_bot_teams(user_region_id)               
                region_leagues = League.query.get(region_id=user_region_id)

def generate_bot_leagues(region_id):
    #Ultima liga en esa region
    last_league = League.query.filter_by(region_id=region_id).order_by(desc(League.id)).first()
    
    #name, league_depth, league_number
    league_depth = last_league.league_depth + 1 # Profundidad de liga nueva
    league_iterations = (last_league.league_number * 4) # Da la cantidad de nuevas ligas a crearse

    for i in range(1, league_iterations):
        new_league = League(
            name =  random_name(),
            league_depth = league_depth,
            league_number = i
        )
        db.session.add(new_league)

    try:
        db.session.commit()
        return jsonify("New leagues created!"), 200
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify("Problem with leagues correct it at once!"), 400

def generate_bot_teams(region_id):
    #name, finances, trainer_id, stadium_id, league_id
    last_league = League.query.filter_by(region_id=region_id).order_by(desc(League.league_id)).first()
    leagues = League.query.filter_by(region_id=region_id, league_depth=last_league.league_depth)

    for league in leagues:
        for i in range(1,8):
            team_name = "JJX " + str(i)
            team = Team(
                name = team_name,
                finances = 150000,
                trainer_id = generate_random_trainer(),
                stadium_id = generate_stadium(team_name),
                league_id = league.league_id
            )
            for i in range(1,16):
                generate_players(team.team_id, region_id)
            db.session.add(team)
    try:
        db.session.commit()
        return jsonify("Team created"), 200
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify("Team is falling apart, morale really low"), 400

def generate_stadium(team_name):
    #name, standard_seats, bleacher_seats, premium_seats, club_seats, box_seats
    stadium = Stadium(
        name = team_name + " Stadium",
        standard_seats = 5000,
        bleacher_seats = 3500,
        premium_seats = 2000,
        club_seats = 500, 
        box_seats = 50
    )
    db.session.add(stadium)

    try:
        db.session.commit()
        return stadium.stadium_id
    except Exception as e:
        print(e.args)    
        db.session.rollback()
        return jsonify("Transaction couldnt be completed"), 400

def generate_random_trainer():
    #name, trainertype_id
    trainer = Trainer (
        name = random_name(),
        trainertype_id = generate_random_trainer_type()
    )
    db.session.add(trainer)
    try:
        db.session.commit()
        return trainer.trainer_id
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify("This isnt working out!"), 400

def generate_random_trainer_type():
    trainertypes = TrainerType.query.all()
    trainertype=random.choice(trainertypes)
    return trainertype.trainertype_id

def generate_players(team_id, region_id):
    #name, age, mentality, speed, passes, shoot, stop_ball, defense, physique, precision, goalkeep, salary, team_id, region_id
    #age between 17 y 26, not too old, not too young
    mentality = random_generator(1,6),
    speed = random_generator(1,6),
    passes = random_generator(1,6),
    shoot = random_generator(1,6),
    stop_ball = random_generator(1,6),
    defense = random_generator(1,6),
    physique = random_generator(1,6),
    precision = random_generator(1,6),
    goalkeep = random_generator(1,6),
    attributes_list = [mentality, speed, passes, shoot, stop_ball, defense, physique, precision, goalkeep]

    player = Player(
        name = random_name(),
        age = random_generator(17,26),
        mentality = mentality,
        speed = speed,
        passes = passes,
        shoot = shoot,
        stop_ball = stop_ball,
        defense = defense,
        physique = physique,
        precision = precision,
        goalkeep = goalkeep,
        salary  = calculate_salary_based_attributes(attributes_list),
        team_id = team_id,
        region_id = region_id
    )
    db.session(player)

    try:
        db.session.commit()
        return jsonify("Players created"), 200
    except Exception as e:
        print(e.args)
        db.session.rollback()
        return jsonify("Player error, check terminal"), 400

@api.route('/login', methods=['POST'])
def user_login():
    data = request.json
    if data.get("email", None) is None:
        return jsonify({"message": "Email is required"}), 400
    
    user = User.query.filter_by(email=data["email"]).one_or_none()
    if user is not None:
        result = check_password_hash(user.password, f'{data["password"]}{user.salt}')
        if result:
            token = create_access_token(identity=user.email)
            return jsonify({"token":token}), 200
        else: 
            return jsonify({"message": "bad credentials"}), 400
    else: 
        return jsonify({"message": "bad credentials"}), 400

    