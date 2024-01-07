import yaml


def load_config(dir="config.YAML"):
    with open(dir, "r") as f:
        return yaml.safe_load(f)
