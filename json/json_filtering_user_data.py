### JSON FILTERING -- USER DATA ### 

import json
### RULES
groups_struc           = {} ### YANG CONTAINER
groups_struc['groups'] = [] ### [group_dict]
group_dict             = {} ### YANG LEAF {"group": {group_name": "G" , "members": member_list} }                             
group_list             = [] ### YANG LIST [group_dict]
member_dict            = {} ### YANG LEAF  {"person_name": "x", "email": "y", "group":"z" }
member_list            = [] ### YANG LIST [member_dict]

###
groups_struc = {
 "groups": [
      { "group": { "group_id": "G1" , "group_name": "GROUP_MICRO" ,    
                   "members": [   
                     {"person_id": "P-1" , "person_name": "Nick", "email": "nick@biasc.be"},
                     {"person_id": "P-2" , "person_name": "Marcus", "email": "marcus@biasc.be"},
                     {"person_id": "P-3" , "person_name": "Liesbet", "email": "liesbet@biasc.be"} 
                   ]
                 }
      },
      { "group": { "group_id": "G2" , "group_name": "GROUP_NANO" ,    
                   "members": [   
                     {"person_id": "P-4" ,"person_name": "Martin", "email": "martin@biasc.be"}, 
                     {"person_id": "P-5" ,"person_name": "Bob", "email": "bob@biasc.be"}, 
                     {"person_id": "P-6" ,"person_name": "Alice", "email": "alice@biasc.be"} 
                   ]     
                 }
      },
      { "group": { "group_id": "G3" , "group_name": "GROUP_PICO" ,    
                   "members": [   
                     {"person_id": "P-7" ,"person_name": "Matt", "email": "matt@biasc.be"}, 
                     {"person_id": "P-8" ,"person_name": "Lucas", "email": "lucas@biasc.be"}, 
                     {"person_id": "P-9" ,"person_name": "Elsa", "email": "elsa@biasc.be"} 
                   ] 
                 }
      }
   ]
}

print('------1---------')
print(type(groups_struc))
print(groups_struc)
print('------1A--------')
# convert dict to json
js_groups = json.dumps(groups_struc)
print(type(js_groups))
print(js_groups)
#print(json.dumps(groups_struc, indent=2))

print('------2---------')
for g in groups_struc["groups"]:
    print('------2A--------')
    print(type(g))
    print(g)
    print('------2B--------')
    print(g["group"]["group_name"])
    print('------2C--------')
    for p in g["group"]["members"]:
        print(p["person_name"] + " => " + p["email"])
            
print('------3---------')
print(groups_struc.keys())
print('------3A---------')
print(groups_struc["groups"][0].keys())
print('------3B---------')
print(groups_struc["groups"][0]["group"].keys())
print('------3C---------')
print(groups_struc["groups"][0]["group"]["members"][0].keys())
