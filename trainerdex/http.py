import json
import logging
import requests
import sys
from typing import Union
from urllib.parse import quote

from trainerdex import __version__

log = logging.getLogger("trainerdex.http")

def json_or_text(response: requests.Response) -> Union[dict, str]:
    try:
        return response.json()
    except ValueError:
        return response.text

class Route:
    BASE = 'https://www.trainerdex.co.uk/api/v1'
    
    def __init__(self, method, path, **parameters):
        """Thanks to Rapptz for this implementation!
        
        Dear Rapptz,
        
        If you ever see this code, welcome. I took great inspiration from your
        discord.py async branch when developing this code. If we ever meet
        I will buy you a coffee and maybe a bagel
        
        Thank you,
        Jay Turner
        
        The MIT License (MIT)

        Copyright (c) 2015-2020 Rapptz

        Permission is hereby granted, free of charge, to any person obtaining a
        copy of this software and associated documentation files (the "Software"),
        to deal in the Software without restriction, including without limitation
        the rights to use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to whom the
        Software is furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
        OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
        DEALINGS IN THE SOFTWARE.
        """
        
        self.path = path
        self.method = method
        url = (self.BASE + self.path)
        if parameters:
            self.url = url.format(**{k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        else:
            self.url = url


class HTTPClient:
    """HTTP Client for sending HTTP request to the API"""
    
    def __init__(self, token: str = None):
        self.token = token
        
        user_agent = 'trainerdex.py (https://github.com/TrainerDex/TrainerDex.py {0}) Python/{1[0]}.{1[1]} requests/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, requests.__version__)
    
    def request(self, route: Route, **kwargs):
        """Make a request
        
        Parameters
        ----------
        route: trainerdex.http.Route
        params: dict, optional
            Dictionary, list of tuples or bytes to send in the query string for the Request
        data: dict, optional
            Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request
        json: dict, optional
            A JSON serializable Python object to send in the body of the Request
        
        Raises
        ------
        requests.HTTPError
        
        """
        method = route.method
        url = route.url
        
        headers = {
            'User-Agent': self.user_agent,
        }
        
        if self.token is not None:
            headers['authorization'] = 'Token {}'.format(self.token)
        
        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(kwargs.pop('json'))
        
        kwargs['headers'] = headers
        
        with requests.request(method, url, **kwargs) as r:
            log.debug('{} {} with {} has returned {}'.format(method, url, kwargs.get('data'), r.status_code))
            
            data = json_or_text(r)
            
            if 200 <= r.status_code < 300:
                log.debug('{} {} has received {}'.format(method, url, data))
                return data
            elif 400<= r.status_code < 600:
                r.raise_for_status()
