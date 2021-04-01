import pytest
import connexion
from app import home
#from app import app

flask_app = connexion.FlaskApp(__name__, specification_dir='./openapi')
flask_app.add_api('./base.yaml')
flask_app.testing = True

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c

def test_home(client):
    """ Test home endpoint returns 200    
    """
    response = client.get('index.html')
    assert response.status_code == 200

def test_favicon(client):
    """ Test favicon endpoint returns 200    
    """
    response = client.get('/favicon.ico')
    assert response.status_code == 200
