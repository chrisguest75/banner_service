import connexion
from prometheus_flask_exporter import ConnexionPrometheusMetrics
from .flask_request_intercepts import flask_intercepts

# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir='./openapi')
metrics = ConnexionPrometheusMetrics(app)


# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yaml', validate_responses=False)
handlers = flask_intercepts(app)