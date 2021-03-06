import pytest
import connexion

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('./openapi/swagger.yaml')
flask_app.testing = True

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_ready(client):
    """ Test ready endpoint returns 200    
    """
    response = client.get('/api/ready')
    assert response.json == "Ready"    
    assert response.status_code == 200


