from connexion import NoContent
from app import metrics

@metrics.summary('ready_by_status', 'ready Request latencies by status', labels={
    'code': lambda r: r.status_code
})
def ready():
    return "Ready", 200