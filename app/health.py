from connexion import NoContent
from app import metrics
import subprocess
import logging

def dependency_check():
    logger = logging.getLogger()
    try:
        completed = subprocess.run(["jp2a", "--version"], capture_output=True)
        if completed.returncode != 0:
            logger.debug(f"jp2a not found in environment", extra={})
            return False
        else:    
            logger.debug(f"jp2a found in environment", extra={"version": completed.stdout})
            return True
    except subprocess.CalledProcessError as e:
        logger.debug(f"jp2a not found in environment", extra={})
        return False

@metrics.summary('health_by_status', 'health Request latencies by status', labels={
    'code': lambda r: r.status_code
})
def health():
    if dependency_check():
        return "Healthy", 200        
    else:
        return "Unhealthy", 503            
