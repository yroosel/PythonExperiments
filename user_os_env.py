# Python program to explain os.environ object 
# importing os and pprint module 
import os
import pprint 
# Get the list of user's environment variables
env_var = os.environ
#Play width the output based on examples below
#Print the list of user's environment variables
#print("User's Environment variable:")
#pprint.pprint(dict(env_var), width = 1)
print("===============")
print("PATH User's Environment:")
print(env_var['PATH'])
