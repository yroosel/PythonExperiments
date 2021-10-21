####  DELETE WEBEX "DEMO" SPACES
from webexteamssdk import WebexTeamsAPI
### Access Token 12 hours: https://developer.webex.com/docs/api/getting-started (login required)
current_access_token = "YjU0MGQ4ZDgtMDk2NC00ZjAxLWE3YzktMjNjYTA2NzFmZmE0MzBmZTUyOGMtMmQ5_PF84_e4d4112d-2548-4a47-810e-04fe45ea181f"
access_token = current_access_token 
api = WebexTeamsAPI(access_token=access_token)
# Find all rooms that should be removed
all_rooms = api.rooms.list()

demo_rooms = [room for room in all_rooms if 'GROUP_YRO_' in room.title]

# Delete all of the demo rooms
for room in demo_rooms:
    print("Deleting ... " + room.title)
    api.rooms.delete(room.id)
