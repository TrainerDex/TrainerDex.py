import requests

api_url = 'http://www.ekpogo.uk/api/trainer/'

def request_status(r):
	"""Returns a formatted string about the status, useful for logging.
	
	args:
	r - takes requests.models.Response
	"""
	
	base_string = "HTTP {r.request.method} {r.request.url}: {r.status_code}"
	
	if r.status_code==requests.codes.ok:
		string = base_string
		if detailed is True:
			string += " - {r.json()}"
		else:
			string += " - All is okay. I'm not a teapot."
		return string.format(r)
	elif r.status_code==request.codes.teapot:
		string = base_string
		if detailed is True:
			string += "{r.json()}"
		else:
			string += " I'm a little teapot, short and stout. Here is my handle, here is my spout. When I get all steamed up, hear me shout! Just tip me over and pour me out."
		return string.format(r)
	else:
		string = base_string
		string += "{r.json()}"
		return string.format(r)