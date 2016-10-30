import os
import json

env_var_name = "PYUTILS"

settings_path = os.getenv(env_var_name, "")
if len(settings_path) < 1:
    settings_path = os.path.dirname(os.path.realpath(__file__)) + "/../resources/settings.json"
else:
    settings_path += "/settings.json"


def read_parameter(name):
    read_data = ""
    with open(settings_path, 'r') as f:
        read_data = f.read()
    json_content = json.loads(read_data)
    return json_content[name]


class Settings:
    def __init__(self):
        pass

    pem_file_path = read_parameter("pemFileParh")
    splice_dir_cloudera = read_parameter("spliceDirCloudera")
    splice_dir_mapr = read_parameter("spliceDirMapr")
    splice_dir_horton = read_parameter("spliceDirHorton")
