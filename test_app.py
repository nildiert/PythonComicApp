from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS


import json

import urllib.request
from urllib.error import HTTPError


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():

    api_key = '5254c165a43cf4186f83c78079d1bcff35f1c751'
    url = 'https://comicvine.gamespot.com/api/issues/?api_key={}&sort=cover_date:desc&format=json&sort=cover_date:desc'.format(api_key)

    try:
        with urllib.request.urlopen(url) as response:
            jsonResponse = json.loads(response.read().decode('utf-8'))

            result = jsonResponse.get('results')
            comic_list = []
            comics = {}

            for item in result:
                comic_item = {}
                id_comic = item['id']
                img = item['image']['original_url']
                date = item['date_added']
                name = ("{} #{}".format(item['volume']['name'], item['issue_number']))
                comic_item.update({"id": id_comic, "name": name, "date": date, "image": img})
                comic_list.append(comic_item)

            comics.update({'data':comic_list})

            return comics
    except HTTPError as e:
        return {"Error code": "{}".format(e.code)}
    except:
        pass


if __name__ == '__main__':
    app.run(debug = True)


