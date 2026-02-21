import os
import logging
from datetime import datetime

LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f'log_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

def get_logger(name):
    """
    Get a logger instance configured to log at INFO level and above.
    
    Args:
        name (str): Logger name, typically __name__ of the calling module
        
    Returns:
        logging.Logger: Configured logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("This is a log message")
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger