import requests 
import json 
### Access Token 12 hours: https://developer.webex.com/docs/api/getting-started (login required)
access_token = "insert your own token"

groups_struc = {
 "groups": [
      { "group": { "group_id": "G1" , "group_name": "GROUP_YRO_A" ,    
                   "members": [   
                     {"person_id": "P-1" , "person_name": "Nick", "email": "nick@biasc.be"},
                     {"person_id": "P-2" , "person_name": "Marcus", "email": "marcus@biasc.be"},
                     {"person_id": "P-3" , "person_name": "Lisa", "email": "lisa@biasc.be"} 
                   ]
                 }
      },
      { "group": { "group_id": "G2" , "group_name": "GROUP_YRO_B" ,    
                   "members": [   
                     {"person_id": "P-4" ,"person_name": "Martin", "email": "martin@biasc.be"}, 
                     {"person_id": "P-5" ,"person_name": "Bob", "email": "bob@biasc.be"}, 
                     {"person_id": "P-6" ,"person_name": "Alice", "email": "alice@biasc.be"} 
                   ]     
                 }
      },
      { "group": { "group_id": "G3" , "group_name": "GROUP_YRO_C" ,    
                   "members": [   
                     {"person_id": "P-7" ,"person_name": "Matt", "email": "matt@biasc.be"}, 
                     {"person_id": "P-8" ,"person_name": "Lucas", "email": "lucas@biasc.be"}, 
                     {"person_id": "P-9" ,"person_name": "Elsa", "email": "elsa@biasc.be"} 
                   ] 
                 }
      }
   ]
}

url = 'https://api.ciscospark.com/v1/rooms'

headers = {'Authorization': 'Bearer {}'.format(access_token),'Content-Type': 'application/json' }
for rec in groups_struc["groups"]:
    create_group_name = rec["group"]["group_name"]
    print("Creating ... " + create_group_name)
    payload_space={"title": create_group_name}
    res_space = requests.post(url, headers=headers, json=payload_space)

    NEW_SPACE_ID = res_space.json()["id"]
    for mbr in rec["group"]["members"]:
        room_id = NEW_SPACE_ID
        person_email = mbr["email"] 
        url2 = 'https://api.ciscospark.com/v1/memberships'
        payload_member = {'roomId': room_id, 'personEmail': person_email}
        res_member = requests.post(url2, headers=headers, json=payload_member)

