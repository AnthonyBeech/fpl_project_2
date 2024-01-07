import logging
import os
from datetime import datetime

from src.utils import load_config

cfg = load_config()
log_folder = cfg["logs_dir"]


# create dir to store log files
logs_dir = os.path.join(os.getcwd(), log_folder)
os.makedirs(logs_dir, exist_ok=True)

# Define log file name with current timestamp
log_file_name = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
log_file_path = os.path.join(logs_dir, log_file_name)


# Configure logging
logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Test logging
logging.info("Logger initialized.")
