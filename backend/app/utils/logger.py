import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create log filename with timestamp
log_filename = f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
log_filepath = os.path.join(logs_dir, log_filename)

# Configure logging format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(log_format)

# Create and configure FileHandler
file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Create and configure StreamHandler (console output)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
