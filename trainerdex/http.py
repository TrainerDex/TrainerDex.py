import requests

API_BASE_URL = 'https://www.trainerdex.co.uk/api/v1/'


def request_status(response: requests.models.Response, detailed: bool = False) -> str:
    """Returns a formatted string about the status, useful for logging.
    
    Parameters
    ----------
    r: requests.models.Response
    
    Returns
    -------
    string
    """
    
    base_string = "HTTP {response.request.method} {response.request.url}: {response.status_code}"
    
    if response.status_code in range(200, 99):
        string = base_string
        if detailed:
            string += " - {response.json()}"
        else:
            string += " - 👍"
        return string.format(response=response)
    else:
        string = base_string
        return string.format(response=response)
