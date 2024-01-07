import os
import yaml
import pytest
import tempfile
from src.utils import load_config

test_config = {"key": "value", "number": 42}

def test_load_config_valid():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        yaml.dump(test_config, f)
        temp_config_path = f.name

    config = load_config(temp_config_path)
    assert config == test_config

    os.remove(temp_config_path)  # Cleanup the temporary file

def test_load_config_missing():
    with tempfile.NamedTemporaryFile() as f:
        temp_config_path = f.name

    # File is deleted once the with block is exited
    with pytest.raises(FileNotFoundError):
        config = load_config(temp_config_path)