from app import db, Hero, Power

def test_create_hero(client, session):
    response = client.post('/heroes', json={'name': 'Test Hero', 'super_name': 'The Tester'})
    assert response.status_code == 201
    assert response.json['message'] == 'Hero created successfully!'

def test_get_hero(client, session):
    hero = Hero(name='Test Hero', super_name='The Tester')
    session.add(hero)
    session.commit()

    response = client.get(f'/heroes/{hero.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Hero'
    assert response.json['super_name'] == 'The Tester'

def test_create_power(client, session):
    response = client.post('/powers', json={'name': 'Test Power', 'description': 'This is a test power with more than 20 characters.'})
    assert response.status_code == 201
    assert response.json['message'] == 'Power created successfully!'

def test_get_power(client, session):
    power = Power(name='Test Power', description='This is a test power with more than 20 characters.')
    session.add(power)
    session.commit()

    response = client.get(f'/powers/{power.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Power'
    assert response.json['description'] == 'This is a test power with more than 20 characters.'

def test_update_power(client, session):
    power = Power(name='Test Power', description='This is a test power with more than 20 characters.')
    session.add(power)
    session.commit()

    new_description = 'This is an updated test power description with more than 20 characters.'
    response = client.patch(f'/powers/{power.id}', json={'description': new_description})
    assert response.status_code == 200
    assert response.json['description'] == new_description