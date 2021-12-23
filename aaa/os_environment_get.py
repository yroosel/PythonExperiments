#### pip install python-decouple
import os
from decouple import config
# Get the list of user's environment variables
env_var = os.environ
# Experiment with the output based on examples below
print("===============")
print("User Environment")
print("PATH")
print(env_var.get('PATH'))
####
print("USER")
API_USERNAME = config('RESTCONFUSER')
API_PASSWORD = config('RESTCONFPASW')
print(API_USERNAME)
print(API_PASSWORD)

