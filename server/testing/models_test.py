from app import db, Hero, Power

def test_create_hero(session):
    hero = Hero(name='Test Hero', super_name='The Tester')
    session.add(hero)
    session.commit()

    assert hero.id is not None
    assert hero.name == 'Test Hero'
    assert hero.super_name == 'The Tester'

def test_create_power(session):
    power = Power(name='Test Power', description='This is a test power with more than 20 characters.')
    session.add(power)
    session.commit()

    assert power.id is not None
    assert power.name == 'Test Power'
    assert power.description == 'This is a test power with more than 20 characters.'

def test_hero_to_dict(session):
    hero = Hero(name='Test Hero', super_name='The Tester')
    session.add(hero)
    session.commit()

    hero_dict = hero.to_dict()
    assert hero_dict['id'] == hero.id
    assert hero_dict['name'] == 'Test Hero'
    assert hero_dict['super_name'] == 'The Tester'

def test_power_to_dict(session):
    power = Power(name='Test Power', description='This is a test power with more than 20 characters.')
    session.add(power)
    session.commit()

    power_dict = power.to_dict()
    assert power_dict['id'] == power.id
    assert power_dict['name'] == 'Test Power'
    assert power_dict['description'] == 'This is a test power with more than 20 characters.'