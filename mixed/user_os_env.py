# Python program to explain os.environ object 
# importing os and pprint module 
import os
# Get the list of user's environment variables
env_var = os.environ
# Experiment with the output based on examples below
print("===============")
print("PATH User's Environment:")
print(env_var['PATH'])
