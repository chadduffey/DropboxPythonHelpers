import csv
import json
import requests
import sys

t = "token goes here"

cursor_limit = 1000

#---------------
# Business API
#---------------

def get_member_information(token, cursor):
	response = members_list(token)
	
	if not response == False:
		members = response["members"]
		while response['has_more'] == True:
			print "has more..."
			response = members_list_continue(token, response["cursor"])
			members = members + response["members"]
		
		return members

	return False

def members_list(token):
	dfbToken = "Bearer " + token
	data = {"limit": cursor_limit }
    
	try:
		response = requests.post(url='https://api.dropboxapi.com/2/team/members/list',
        					data=(json.dumps(data)),
		                    headers = ({ "Authorization" : dfbToken , "Content-Type": "application/json" }))

		return response.json()
    
	except:
		return False

def members_list_continue(token, cursor):
	dfbToken = "Bearer " + token
	data = { "cursor" : cursor }

	try:
		response = requests.post(url='https://api.dropboxapi.com/2/team/members/list/continue',
        					data=(json.dumps(data)),
		                    headers = ({ "Authorization" : dfbToken , "Content-Type": "application/json" }))

		return response.json()
    
	except:
		return False

def get_group_information(token):
	dfbToken = "Bearer " + token

	try:
		response = requests.post(url='https://api.dropboxapi.com/2/team/groups/list',
		                    headers = ({ "Authorization" : dfbToken  }))

		return response.json()
    
	except:
		return False

#---------------
# Core API
#---------------

def list_folder_content(token, dfb_user_id, folder_path):
	dfbToken = "Bearer " + token
	data="{\"path\": \"" + folder_path + "\",\"recursive\": true,\"include_media_info\": false,\"include_deleted\": false}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/files/list_folder',
	    				data=data,
	                    headers = ({ "Authorization" : dfbToken, 
	                    				"Content-Type" : "application/json" , 
	                    				"Dropbox-API-Select-User" : dfb_user_id }))
	except:
		return False

	return response.json()

def make_shared_folder(token, dfb_user_id, folder_path):
	userToken = "Bearer " + token
	data = "{\"path\": \"" + folder_path + "\",\"acl_update_policy\": \"editors\",\"force_async\": false}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/sharing/share_folder',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, 
	                    				"Content-Type" : "application/json", 
	                    				"Dropbox-API-Select-User" : dfb_user_id }))
	except:
		return False

	return response.json()

def add_share_permissions(token, dfb_user_id, shared_folder_id, group_id, access_level):
	userToken = "Bearer " + token
	data="{\"shared_folder_id\": \"" + shared_folder_id + "\",\"members\": [{\"member\": {\".tag\": \"dropbox_id\",\"dropbox_id\": \"" + group_id + "\"},\"access_level\": {\".tag\": \"" + access_level +"\"}}]}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/sharing/add_folder_member',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, 
	                    				"Content-Type" : "application/json",
	                    				"Dropbox-API-Select-User" : dfb_user_id }))
	except:
		return False

	return response.json()

#---------------
# Non-API 
#---------------

def get_user_detail(all_users, email_to_find):
	for member in all_users:
		if member["profile"]["email"] == email_to_find:
			print "Email: " + member["profile"]["email"]
			print "Member Id: " + member["profile"]["team_member_id"]
			print "Status: " + member["profile"]["status"][".tag"]
			return member["profile"]["team_member_id"]
	return "user not found"

#---------------
# Scenarios
#---------------

# 1. gather all users.
print ""
print "Fetching team information:"
all_team_users = get_member_information(t, None)
if all_team_users:
	print "Sucessfully retrieved " + str(len(all_team_users)) + " users."

# 2. tell me about... by email address and return id
#print ""
#print "Locating Specific User:"
#get_user_detail(all_team_users, "chad@hanfordinc.com")

#3. List content in an account
#print ""
#print "Listing Content:"
#user_content = list_folder_content(t, "dbmid:AAD4Sk-oiD5z5rrlhIYyeZKSPPBhfZ2nHGk", "")
#if not user_content == False:
#	for entry in user_content["entries"]:
#		print entry[".tag"] + " = " + entry["path_display"]

#4. Make a folder a shared folder
#print ""
#print "Sharing a folder:"
#status = make_shared_folder(t, "dbmid:AAD4Sk-oiD5z5rrlhIYyeZKSPPBhfZ2nHGk", "/Subject ITC101")
#print str(status)

#5. Share with group
#print ""
#print "Sharing with group."
#status = add_share_permissions(t, "dbmid:AAD4Sk-oiD5z5rrlhIYyeZKSPPBhfZ2nHGk", "1195490680", 
#								"g:df65a9f15d1d676f000000000001b3c6", "editor")
#print str(status)

#6. Get all the groups
print ""
print "Getting all the Group Id's:"
all_groups = get_group_information(t)
for group in all_groups["groups"]:
	print "Group Name: " + group["group_name"]
	print "Group Id: " + group["group_id"]
	print "Group Member Count: " + str(group["member_count"])
	print ""

if all_groups["has_more"] == True:
	print "There were more in there to grab."








