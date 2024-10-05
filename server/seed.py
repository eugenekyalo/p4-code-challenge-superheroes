from random import choice as rc
from app import app
from models import db, Hero, Power, HeroPower

# Function to seed the database
def seed_database():
    with app.app_context():
        # Clear the database
        print("Clearing db...")
        HeroPower.query.delete()
        Hero.query.delete()
        Power.query.delete()
        db.session.commit()

        # Seed powers
        print("Seeding powers...")
        powers = [
            Power(name="super strength", description="Gives the wielder super-human strength."),
            Power(name="flight", description="Grants the ability to fly at supersonic speeds."),
            Power(name="super human senses", description="Enhances senses to a super-human level."),
            Power(name="elasticity", description="Allows the body to stretch to extreme lengths."),
            Power(name="invisibility", description="Enables the wielder to become invisible at will."),
        ]
        db.session.add_all(powers)
        db.session.commit()  # Commit the powers to the database

        # Seed heroes
        print("Seeding heroes...")
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)
        db.session.commit()  # Commit the heroes to the database

        # Assign powers to heroes
        print("Assigning powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []

        # Loop through each hero and randomly assign a power with random strength
        for hero in heroes:
            assigned_power = rc(powers)  # Randomly select a power for the hero
            strength = rc(strengths)     # Randomly select a strength level
            hero_power = HeroPower(hero_id=hero.id, power_id=assigned_power.id, strength=strength)
            hero_powers.append(hero_power)

        db.session.add_all(hero_powers)
        db.session.commit()  # Commit all hero powers to the database

        print("Database seeding complete!")

# Run the seeding function when script is executed
if __name__ == '__main__':
    seed_database()
