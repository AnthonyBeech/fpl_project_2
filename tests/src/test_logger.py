import os
from datetime import datetime

from src.logger import logging


def test_logger_setup():
    # Create a tmp logs dir
    logs_dir = "tests/logs"

    #setup_logger(logs_dir)
    logging.info("test")

    # Check if the logs directory is created
    assert os.path.exists(logs_dir) and os.path.isdir(
        logs_dir
    ), "Logs directory should be created"

    # Check for the existence of a log file with the expected timestamp
    timestamp_format = "%Y_%m_%d"
    expected_file_prefix = datetime.now().strftime(timestamp_format)

    log_files = [f for f in os.listdir(logs_dir) if f.startswith(expected_file_prefix)]

    assert len(log_files) > 0, "Log file with today's date should be created"

    # Clean up by removing the created log files and directory
    for file in log_files:
        os.remove(os.path.join(logs_dir, file))
    os.rmdir(logs_dir)
