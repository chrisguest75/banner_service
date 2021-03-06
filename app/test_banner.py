import pytest
import connexion

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('./swagger.yaml')
flask_app.testing = True

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_generate(client):
    """ Test generate endpoint returns 200    
    """
    response = client.get('/api/banner?message=whatever&fontname=cuddly&width=100')
    assert response.status_code == 200

