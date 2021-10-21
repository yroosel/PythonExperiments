####  DELETE WEBEX "DEMO" SPACES
from webexteamssdk import WebexTeamsAPI
### Access Token 12 hours: https://developer.webex.com/docs/api/getting-started (login required)
access_token = "insert your own token"
api = WebexTeamsAPI(access_token=access_token)
# Find all rooms that should be removed
all_rooms = api.rooms.list()

demo_rooms = [room for room in all_rooms if 'GROUP_YRO_' in room.title]

# Delete all of the demo rooms
for room in demo_rooms:
    print("Deleting ... " + room.title)
    api.rooms.delete(room.id)
