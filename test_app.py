from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import render_template


import json

import urllib.request
from urllib.error import HTTPError


app = Flask(__name__)
CORS(app)


@app.route('/comics', methods=['GET'])
def index():

    api_key = '5254c165a43cf4186f83c78079d1bcff35f1c751'
    url = 'https://comicvine.gamespot.com/api/issues/?api_key={}&sort=cover_date:desc&format=json&sort=cover_date:desc'.format(api_key)

    try:
        with urllib.request.urlopen(url) as response:
            jsonResponse = json.loads(response.read().decode('utf-8'))

            result = jsonResponse.get('results')
            comic_list = []

            for item in result:
                comic_item = {}
                id_comic = item['id']
                img = item['image']['original_url']
                date = item['date_added']
                name = ("{} #{}".format(item['volume']['name'], item['issue_number']))
                comic_item.update({"id": id_comic, "name": name, "date": date, "image": img})
                comic_list.append(comic_item)

            context = {
                'comics': comic_list
            }

            # return comics
            return render_template('index.html', **context)


    except HTTPError as e:
        return {"Error code": "{}".format(e.code)}
    except:
        pass

@app.route('/comic/<id>')
def view_comic(id):
    api_key = '5254c165a43cf4186f83c78079d1bcff35f1c751'
    url = 'https://comicvine.gamespot.com/api/issue/4000-{}/?api_key={}&sort=cover_date:desc&format=json&sort=cover_date:desc'.format(id, api_key)


    try:
        with urllib.request.urlopen(url) as response:
            jsonResponse = json.loads(response.read().decode('utf-8'))

            result = jsonResponse.get('results')
            # comic_list = []

            return result

            # context = {
            #     'comics': comic_list
            # }

            # return comics
            # return render_template('index.html', **context)
    except HTTPError as e:
        return {"Error code": "{}".format(e.code)}
    except:
        pass

    return render_template('show.html')



if __name__ == '__main__':
    app.run(debug = True)


