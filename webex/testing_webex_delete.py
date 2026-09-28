from webexpythonsdk import WebexAPI

access_token = "Your Access Token"

api = WebexAPI(access_token=access_token)

# Get all spaces
all_rooms = api.rooms.list()

# Select the GROUP_YRO_ spaces
demo_rooms = [
    room for room in all_rooms
    if "GROUP_YRO_" in room.title
]

for room in demo_rooms:
    print("Deleting:", room.title)
    api.rooms.delete(room.id)
