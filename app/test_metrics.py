import pytest
import connexion
from prometheus_flask_exporter import ConnexionPrometheusMetrics

# Create the application instance
flask_app = connexion.FlaskApp(__name__)
metrics = ConnexionPrometheusMetrics(flask_app)
flask_app.add_api('./openapi/swagger.yaml')
flask_app.testing = True

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_metrics(client):
    """ Test metrics endpoint returns 200    
    """
    response = client.get('/metrics')
    assert response.status_code == 200


