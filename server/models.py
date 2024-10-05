from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    powers = db.relationship('HeroPower', backref='hero', cascade='all, delete')

    # Serialization rules
    serialize_rules = ('-powers.hero_id',)

    def __repr__(self):
        return f'<Hero {self.name} - {self.super_name}>'

class Power(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters")
        return value

    def __repr__(self):
        return f'<Power {self.name}>'

class HeroPower(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return value

    def __repr__(self):
        return f'<HeroPower {self.strength}>'
