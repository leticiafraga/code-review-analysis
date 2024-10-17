import logging
import time


def setup_logging():
    logging.basicConfig(
        filename='logs/github_analysis.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_error(e):
    logging.error(e)

def retry_on_failure(max_retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    log_error(f"Attempt {retries} failed with error: {e}")
                    if retries < max_retries:
                        time.sleep(delay)
                    if retries == max_retries:
                        raise
        return wrapper
    return decorator
