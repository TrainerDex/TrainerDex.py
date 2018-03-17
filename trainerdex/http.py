import requests

api_url = 'https://www.trainerdex.co.uk/api/v1/'

def request_status(r, detailed=False):
	"""Returns a formatted string about the status, useful for logging.
	
	args:
	r - takes requests.models.Response
	"""
	
	base_string = "HTTP {r.request.method} {r.request.url}: {r.status_code}"
	
	if r.status_code in range(200,99):
		string = base_string
		if detailed is True:
			string += " - {r.json()}"
		else:
			string += " - 👍"
		return string.format(r=r)
	else:
		string = base_string
		return string.format(r=r)
