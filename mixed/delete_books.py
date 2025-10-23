import requests
import json

APIHOST = "http://library.demo.local"
LOGIN = "uuuuuuuu"
PASSWORD = "pwpwpwpw!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def deleteBook(book_id, apiKey):
    r = requests.delete(
        f"{APIHOST}/api/v1/books/{book_id}", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            }
    )
    if r.status_code == 200:
        print(f"Book {book_id} deleted.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to delete book {book_id}.")

# Get the Auth Token Key
apiKey = getAuthToken()

# Deleting a range of books
for i in range(900,910):
    book_id = i 
    deleteBook(book_id, apiKey) 

