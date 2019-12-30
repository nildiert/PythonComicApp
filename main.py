from flask import redirect, url_for, render_template, make_response
import json
from urllib.error import HTTPError
from app.data_service import *
from app.config import Config as config
from app import create_app

app = create_app()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def home():
    response = make_response(redirect('/comics'))

    return response

@app.route('/comics', methods=['GET'])
def index():
    issues_url = config.issues_url.format(config.api_key)

    try:
        result = get_data(issues_url)
        for item in result:
            item.update({
                "id": item['id'],
                "name": "{} #{}".format(item['volume']['name'], item['issue_number']),
                "image": item['image']['original_url']
                })
        
        context = {
            'comics': result
        }
        return render_template('index.html', **context)

    except HTTPError as e:
        return {"Error code": "{}".format(e.code)}

@app.route('/comic/<id>')
def show(id):

    comic = {}
    issue_detail_url = config.issue_detail_url.format(id, config.api_key)

    try:
        result = get_data(issue_detail_url)
    
        characters = get_detail_data(result['character_credits'], config.character_url)
        teams = get_detail_data(result['team_credits'], config.team_url)
        locations = get_detail_data(result['location_credits'], config.location_url)

        comic.update({
            'image': result['image']['original_url'],
            'characters': characters,
            'teams': teams,
            'locations': locations,
        })
        context = {
            'comic': comic
        }

        return render_template('show.html', **context)


    except HTTPError as e:
        return {"Error code": "{}".format(e.code)}



if __name__ == '__main__':
    app.run(debug = True)


