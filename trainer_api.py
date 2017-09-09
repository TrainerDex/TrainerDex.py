import discord
import urllib.request

api_domain = "http://127.0.0.1:8000"
api_dir = "/api/trainer"

def api_get(item, args=None):
	request_url = api_domain+api_dir
	request_url = request_url+item+'/'
	
	if args:
		request_url= request_url+args+'/'
			
	return urllib.request.urlopen(request_url).read()

class Requests:
	
	def discordUser(discord):
		return api_get(item='discord/user', args=discord)

