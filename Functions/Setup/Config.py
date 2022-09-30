import yaml

def readConfig(filepath):
    with open(filepath, "r",  encoding='utf-8') as f:
        return yaml.safe_load(f)
