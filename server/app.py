from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    else:
        app.config.update(config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.route('/heroes', methods=['GET'])
    def get_all_heroes():
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes]), 200

    @app.route('/heroes/<int:hero_id>', methods=['GET'])
    def get_hero_by_id(hero_id):
        hero = db.session.get(Hero, hero_id)
        if not hero:
            return jsonify({'error': 'Hero not found.'}), 404
        return jsonify(hero.to_dict()), 200

    @app.route('/powers', methods=['GET'])
    def get_all_powers():
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers]), 200

    @app.route('/powers/<int:power_id>', methods=['GET'])
    def get_power_by_id(power_id):
        power = db.session.get(Power, power_id)
        if not power:
            return jsonify({'error': 'Power not found.'}), 404
        return jsonify(power.to_dict()), 200

    @app.route('/powers/<int:power_id>', methods=['PATCH'])
    def update_power_description(power_id):
        data = request.get_json()
        power = db.session.get(Power, power_id)
        if not power:
            return jsonify({'error': 'Power not found.'}), 404
        description = data.get('description', '')
        if len(description) < 20:
            return jsonify({'error': 'Description must be at least 20 characters long.'}), 400
        power.description = description
        db.session.commit()
        return jsonify(power.to_dict()), 200

    @app.route('/heroes', methods=['POST'])
    def create_hero():
        data = request.get_json()
        if not data.get('name') or not data.get('super_name'):
            return jsonify({'error': 'Both name and super_name are required fields.'}), 400
        new_hero = Hero(name=data['name'], super_name=data['super_name'])
        db.session.add(new_hero)
        db.session.commit()
        return jsonify({'message': 'Hero created successfully!'}), 201

    @app.route('/powers', methods=['POST'])
    def create_power():
        data = request.get_json()
        if not data.get('name') or not data.get('description'):
            return jsonify({'error': 'Both name and description are required fields.'}), 400
        if len(data['description']) < 20:
            return jsonify({'error': 'Description must be at least 20 characters long.'}), 400
        new_power = Power(name=data['name'], description=data['description'])
        db.session.add(new_power)
        db.session.commit()
        return jsonify({'message': 'Power created successfully!'}), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)