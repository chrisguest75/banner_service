import pytest
import connexion

flask_app = connexion.FlaskApp(__name__, specification_dir='./openapi')
flask_app.add_api('./swagger.yaml')
flask_app.testing = True

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_health(client):
    """ Test health endpoint returns 200    
    """
    response = client.get('/api/health')
    assert response.json == "Healthy"
    assert response.status_code == 200


