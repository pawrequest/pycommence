import logging
import os
import pytest
from pycommence.logger_config import configure_logging

test_params = [
    (logging.INFO, "Test info message", "INFO - Test info message"),
    (logging.ERROR, "Test error message", "ERROR - Test error message"),
]
@pytest.mark.parametrize("log_level, log_message, expected_message", test_params)
def test_logging(caplog, tmp_path, log_level, log_message, expected_message):
    log_file = tmp_path / "test.log"
    logger = configure_logging(str(log_file), level=log_level)
    logger.log(log_level, log_message)

    assert log_message in caplog.text

    # Verify log file content
    assert os.path.exists(log_file)
    with open(log_file) as file:
        log_contents = file.read()
        assert expected_message in log_contents

    # Clean up
    os.remove(log_file)
