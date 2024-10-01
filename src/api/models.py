from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    salt = db.Column(db.String(200), nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'), nullable=False)
    
    team = db.relationship('Team', back_populates='user', uselist=True)
    region = db.relationship('Region', back_populates='region', uselist=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
        }
    
    def serialize_datafull(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "team": list(map(lambda item: item.serialize(), self.team)),
            "region": list(map(lambda item: item.serialize(), self.region))
        }
    
class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    mentality = db.Column(db.String(42), nullable=False)
    speed= db.Column(db.Intger, nullable=False)
    passes= db.Column(db.Integer, nullable=False)
    shoot= db.Column(db.Integer, nullable=False)
    stop_ball= db.Column(db.Integer, nullable=False)
    defense= db.Column(db.Integer, nullable=False)
    physique= db.Column(db.Integer, nullable=False)
    precision= db.Column(db.Integer, nullable=False)
    goalkeep= db.Column(db.Integer, nullable=False)
    salary=db.Column(db.Integer, nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'), nullable=False)
    
    team = db.relationship('Team', back_populates='user', uselist=True)
    region = db.relationship('Region', back_populates='region', uselist=True)

    def serialize(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "age": self.age,
            "mentality":self.mentality,
            "speed":self.speed,
            "passes":self.passes,
            "shoot":self.shoot,
            "stop_ball":self.stop_ball,
            "defense":self.defense,
            "physique":self.physique,
            "precision":self.precision,
            "goalkeep":self.goalkeep,
            "salary":self.salary   
        }
    
    def serialize_datafull(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "age": self.age,
            "mentality":self.mentality,
            "speed":self.speed,
            "passes":self.passes,
            "shoot":self.shoot,
            "stop_ball":self.stop_ball,
            "defense":self.defense,
            "physique":self.physique,
            "precision":self.precision,
            "goalkeep":self.goalkeep,
            "salary":self.salary,
            "team": list(map(lambda item: item.serialize(), self.team)),
            "region": list(map(lambda item: item.serialize(), self.region))   
        }

class Position(db.Model):
    position_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "name": self.name
        }

class Position_Player(db.Model):
    position_player_id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    
    position = db.relationship('Position', back_populates='position', uselist=True)
    player = db.relationship('Player', back_populates='player', uselist=True)

    def serialize(self):
        return {
            "level": self.level,
            "experience": self.experience
        }
    
    def serialize_datafull(self):
        return {
            "player": list(map(lambda item: item.serialize(), self.player)),   
            "position": list(map(lambda item: item.serialize(), self.position)),
            "level": self.level,
            "experience": self.experience
        }
    
class Region(db.Model):
    region_id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)

    def serialize(self):
        return {
            "region_id": self.region_id,
            "name": self.name
        }
    
class Team(db.Model):
    team_id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    finances= db.Column(db.Integer, nullable=False)

    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id'), nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.stadium_id'), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    
    trainer = db.relationship('Trainer', back_populates='trainer', uselist=True)
    stadium = db.relationship('Stadium', back_populates='stadium', uselist=True)
    league = db.relationship('League', back_populates='league', uselist=True)

    def serialize_datafull(self):
        return{
            "team_id": self.team_id,
            "name": self.name,
            "trainer": list(map(lambda item: item.serialize(), self.trainer)),
            "stadium": list(map(lambda item: item.serialize(), self. stadium)),
            "league": list(map(lambda item: item.serialize(), self.league)),
            "finances": self.finances
        }
    
    def serialize(self):
        return {
           "name": self.name,
           "trainer": list(map(lambda item: item.serialize(), self.trainer))
        }

class Stadium(db.Model):
    stadium_id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), nullable=False)
    standard_seats=db.Column(db.Integer, nullable=False)
    bleacher_seats=db.Column(db.Integer, nullable=False)
    premium_seats=db.Column(db.Integer, nullable=False)
    club_seats=db.Column(db.Integer, nullable=False)
    box_seats=db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "stadium_id": self.stadium_id,
            "name": self.name,
            "standard_seats": self.standard_seats,
            "bleacher_seats": self.bleacher_seats,
            "premium_seats": self.premium_seats,
            "club_seats": self.club_seats,
            "box_seats": self.box_seats
        }

class Trainer(db.Model):
    trainer_id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), nullable=False)

    trainer_type = db.Column(db.Integer, db.ForeignKey('trainer_type.trainer_type_id'), nullable=False) 
    trainer_type = db.relationship('Trainer_Type', back_populates='trainer_type', uselist=True)

    def serialize_datafull(self):
        return {
            "trainer_id": self.trainer_id,
            "name": self.name,
            "trainer_type": list(map(lambda item: item.serialize(), self.trainer_type))
        }
    
class Trainer_Type(db.Model):
    trainer_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    attribute_increase = db.Column(db.String(120), nullable=False)
    increase_amount = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return{
            "name": self.name,
            "attribute_increase": self.attribute_increase,
            "increase_amount": self.increase_amount
        }
    
class League(db.Model):
    league_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False)
    league_depth=db.Column(db.Integer, nullable=False)
    league_number=db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "league_id": self.league_id,
            "name": self.name,
            "league_depth": self.league_depth,
            "league_number": self.league_number
        }
    
class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    match_date = db.Column(db.Integer, nullable=False)
    
    league_id = db.Column(db.Integer, db.Foreignkey('league.league_id'), nullable=False)
    home_team = db.Column(db.Integer, db.Foreignkey('team.team_id'), nullable=False)
    away_team = db.Column(db.Integer, db.Foreignkey('team.team_id'), nullable=False)

    home_goals = db.Column(db.Integer, nullable=False)
    away_goals = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(120), nullable=False)
    played= db.Column(db.Boolean, nullable=False)

    home_team = db.relationship('Team', back_populates='home_team', uselist=True)
    away_team = db.relationship('Team', back_populates='away_team', uselist=True)
    league_id = db.relationship('League', back_populates='league_id', uselist=True)

    def serialize(self):
        return {
            "match_date": self.match_date,
            "home_team": list(map(lambda item: item.serialize(), self.home_team)),
            "home_goals": self.home_goals,
            "away_team": list(map(lambda item: item.serialize(), self.away_team)),
            "away_goals": self.away_goals,
            "result": self.result,
            "played": self.played
        }

