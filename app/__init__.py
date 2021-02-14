import connexion
from prometheus_flask_exporter import ConnexionPrometheusMetrics
from .flask_request_intercepts import flask_intercepts

# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir='./')
metrics = ConnexionPrometheusMetrics(app)

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yaml')
handlers = flask_intercepts(app)
