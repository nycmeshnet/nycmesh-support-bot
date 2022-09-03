# Description: Takes 1 arguement with name of environment variable which contains JSON representation of .env secrets and writes actual .env file.  Allows many GitHub Secrets to be passed through into Docker container together without hardcoding.

import json
import sys
import os

args = sys.argv
secrets_var = args[1]

secrets_json_string = os.environ[secrets_var]
secrets = json.loads(secrets_json_string)

f = open(".env", "w")

for key, value in secrets.items():
    # handle secrets that contain newlines and literal special characters 
    value = value.encode("unicode_escape").decode("utf-8")
    value = value.replace(r"\\n", r"\n")
    
    f.write(f"{key}={value}\n")