import json
import urllib.request
from urllib.error import HTTPError
from .config import Config as config

def get_detail_data(data, url):
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
    with urllib.request.urlopen(url) as response:
        jsonResponse = json.loads(response.read().decode('utf-8'))
        return jsonResponse.get('results')


