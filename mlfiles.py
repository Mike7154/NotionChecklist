import yaml
import json
import urllib.parse
from datetime import datetime
import os

def load_yaml_file(file_name):
  # Open the file in read mode
  with open(file_name, "r") as file:
    try:
      # Parse the YAML data and return a Python object
      data = yaml.load(file, Loader=yaml.SafeLoader)
      return data
    except yaml.YAMLError as error:
      # Print the error message if any
      print("Error parsing YAML file:", error)

def load_dict(file):
    f = open(file)
    url_dict = json.load(f)
    f.close()
    return url_dict


def write_dict(file, dictionary):
    with open(file, "w") as convert_file:
        convert_file.write(json.dumps(dictionary))

def create_json(json_file):
    if os.path.isfile(json_file) == False:
        dict = {}
        write_dict(json_file, dict)

def update_log(text):
    now = datetime.now()
    file = "logs.txt"
    timestr = now.strftime('%m/%d/%Y %H:%M:%S')
    log_text = timestr + " : " + text
    f = open(file, "a")
    f.write(log_text+'\n')
    f.close()

def load_setting(section, setting, settings_file = "settings.yml"):
    data = load_yaml_file(settings_file)
    return data[section][setting]

def save_setting(section, setting, value, settings_file = "settings.yml"):
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    with open(settings_file) as fp:
        data = yaml.load(fp)
    data[section][setting] = value
    with open(settings_file, "w") as f:
        yaml.dump(data,f)

def load_all_settings(settings_file = "settings.yml"):
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open(settings_file) as fp:
            data = yaml.load(fp)
        return data

def save_all_settings(data, settings_file = "settings.yml"):
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open(settings_file, "w") as f:
            yaml.dump(data,f)
