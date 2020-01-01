#!/usr/bin/python3
"""
Service to make inquiries to the api
"""

import json
import urllib.request
from urllib.error import HTTPError
from .config import Config as config

def get_detail_data(data, url):
    """
        Returns additional data for /comic/<id> route
        data: Dictionary with main information 
        url: String with the api route. This route can be for characters,
            Teams or Location
    """
    data_list = []
    for item in data:
        resource_url = url.format(item['id'], config.api_key)
        with urllib.request.urlopen(resource_url) as response:
            jsonResponse = json.loads(response.read().decode('utf-8'))
            result = jsonResponse.get('results')
            result['image'] = result['image']['icon_url']
            data_list.append(result)
    
    return data_list

def get_data(url):
    """
        Returns main data for /comics and /comic/<id> routes
        url: String with the api route that includes the api_key
    """
    with urllib.request.urlopen(url) as response:
        jsonResponse = json.loads(response.read().decode('utf-8'))
        return jsonResponse.get('results')


