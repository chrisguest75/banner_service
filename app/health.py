from connexion import NoContent
from app import metrics

@metrics.summary('health_by_status', 'health Request latencies by status', labels={
    'code': lambda r: r.status_code
})
def health():
    return "Healthy", 200