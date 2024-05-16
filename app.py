from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseball_stats.db'
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    game_date = db.Column(db.DateTime, default=datetime.utcnow)
    at_bats = db.Column(db.Integer, nullable=False)
    hits = db.Column(db.Integer, nullable=False)
    home_runs = db.Column(db.Integer, nullable=False)
    walks = db.Column(db.Integer, nullable=False)

@app.route('/team', methods=['POST'])
def create_team():
    data = request.get_json()
    new_team = Team(name=data['name'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify({new_team.id}), 201

@app.route('/team/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = Team.query.get_or_404(team_id)
    return jsonify({'name': team.name})

@app.route('/team/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    data = request.get_json()
    team.name = data['name']
    db.session.commit()
    return jsonify({'name': team.name})

@app.route('/team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'Equipo eliminado.'}), 200

@app.route('/player', methods=['POST'])
def create_player():
    data = request.get_json()
    new_player = Player(name=data['name'], team_id=data['team_id'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({new_player.id}), 201

@app.route('/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get_or_404(player_id)
    return jsonify({'name': player.name, 'team_id': player.team_id})

@app.route('/player/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    player = Player.query.get_or_404(player_id)
    data = request.get_json()
    player.name = data['name']
    player.team_id = data['team_id']
    db.session.commit()
    return jsonify({'name': player.name, 'team_id': player.team_id})

@app.route('/player/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Jugador eliminado.'}), 201

@app.route('/stats', methods=['POST'])
def create_stat():
    data = request.get_json()
    new_stat = PlayerStats(
        player_id=data['player_id'],
        at_bats=data['at_bats'],
        hits=data['hits'],
        home_runs=data['home_runs'],
        walks=data['walks']
    )
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({'id':new_stat.id}), 201

@app.route('/stats/<int:stat_id>', methods=['GET'])
def get_stat(stat_id):
    stat = PlayerStats.query.get_or_404(stat_id)
    return jsonify({'id': stat.id,'player_id': stat.player_id,'at_bats': stat.at_bats,'hits': stat.hits,'home_runs': stat.home_runs,'walks': stat.walks,'game_date': stat.game_date}), 20

@app.route('/stats/<int:stat_id>', methods=['PUT'])
def update_stat(stat_id):
    stat = PlayerStats.query.get_or_404(stat_id)
    data = request.get_json()
    stat.player_id = data['player_id']
    stat.game_date = datetime.strptime(data['game_date'], '%Y-%m-%d')
    stat.at_bats = data['at_bats']
    stat.hits = data['hits']
    stat.home_runs = data['home_runs']
    stat.walks = data['walks']
    db.session.commit()
    return jsonify({'mensaje': 'actualizado exitosamente'}),201

@app.route('/stats/<int:stat_id>', methods=['DELETE'])
def delete_stat(stat_id):
    stat = PlayerStats.query.get_or_404(stat_id)
    db.session.delete(stat)
    db.session.commit()
    return jsonify({'message': 'Estadística eliminada.'}), 200
