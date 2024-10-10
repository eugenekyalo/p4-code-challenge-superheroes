import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()