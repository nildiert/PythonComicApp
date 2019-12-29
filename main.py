from flask import redirect, url_for, render_template, make_response
from flask_cors import CORS
import json
import urllib.request
from urllib.error import HTTPError

from app import create_app


app = create_app()
CORS(app)

@app.route('/')
def index():
    response = make_response(redirect('/comics'))

    return response

@app.route('/comics', methods=['GET'])
def home():

    api_key = '5254c165a43cf4186f83c78079d1bcff35f1c751'
    url = "https://comicvine.gamespot.com/api/issues/?api_key={}&field_list=name,id,date_added,issue_number,image,volume&sort=date_added:desc&format=json".format(api_key)
    

    try:
        with urllib.request.urlopen(url) as response:
            jsonResponse = json.loads(response.read().decode('utf-8'))

            result = jsonResponse.get('results')
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
    except:
        pass

@app.route('/comic/<id>')
def view_comic(id):
    api_key = '5254c165a43cf4186f83c78079d1bcff35f1c751'
    
    url = "https://comicvine.gamespot.com/api/issue/4000-{}/?api_key={}&field_list=location_credits,character_credits,team_credits,image&format=json".format(id, api_key)
    # url = 'https://comicvine.gamespot.com/api/issue/4000-{}/?api_key={}&sort=cover_date:desc&format=json&sort=cover_date:desc'.format(id, api_key)
    character_url = "https://comicvine.gamespot.com/api/character/4005-{}/?api_key={}&field_list=image,name&format=json"
    team_url = "https://comicvine.gamespot.com/api/team/4060-{}/?api_key={}&field_list=image,name&format=json"
    location_url = "https://comicvine.gamespot.com/api/location/4020-{}/?api_key={}&field_list=image,name&format=json"

    try:
        with urllib.request.urlopen(url) as response:
            jsonResponse = json.loads(response.read().decode('utf-8'))

            result = jsonResponse.get('results')
            characters = []
            teams = []
            locations = []
            comic = {}

            for char in result['character_credits']:
                char_url = character_url.format(char['id'], api_key)
                with urllib.request.urlopen(char_url) as char_response:
                    jsonCharResponse = json.loads(char_response.read().decode('utf-8'))
                    char_result = jsonCharResponse.get('results')
                    char_result['image'] = char_result['image']['icon_url']
                    characters.append(char_result)

            for team in result['team_credits']:
                t_url = team_url.format(team['id'], api_key)
                with urllib.request.urlopen(t_url) as team_response:
                    jsonTeamResponse = json.loads(team_response.read().decode('utf-8'))
                    team_result = jsonTeamResponse.get('results')
                    team_result['image'] = team_result['image']['icon_url']
                    teams.append(team_result)

            for location in result['location_credits']:
                loc_url = location_url.format(location['id'], api_key)
                with urllib.request.urlopen(loc_url) as loc_response:
                    jsonLocResponse = json.loads(loc_response.read().decode('utf-8'))
                    loc_result = jsonLocResponse.get('results')
                    loc_result['image'] = loc_result['image']['icon_url']
                    locations.append(loc_result)

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
    except:
        pass

    return render_template('show.html')



if __name__ == '__main__':
    app.run(debug = True)


