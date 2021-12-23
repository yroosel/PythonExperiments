# Python program to explain os.environ object 
# importing os and pprint module 
import os
# Get the list of user's environment variables
env_var = os.environ
# Set environment variables
os.environ['RESTCONFUSER'] = 'cisco'
os.environ['RESTCONFPASW'] = 'cisco123!'
# Experiment with the output based on examples below
print("===============")
print("User Environment")
print("PATH")
#print(env_var['PATH'])
print(env_var.get('PATH'))
print("USER")
print(env_var.get('RESTCONFUSER'))