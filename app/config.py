class Config:
    api_key = '5254c165a43cf4186f83c78079d1bcff35f1c751'
    character_url = "https://comicvine.gamespot.com/api/character/4005-{}/?api_key={}&field_list=image,name&format=json"
    team_url = "https://comicvine.gamespot.com/api/team/4060-{}/?api_key={}&field_list=image,name&format=json"
    location_url = "https://comicvine.gamespot.com/api/location/4020-{}/?api_key={}&field_list=image,name&format=json"
    issues_url = "https://comicvine.gamespot.com/api/issues/?api_key={}&field_list=name,id,date_added,issue_number,image,volume&sort=date_added:desc&format=json"
    issue_detail_url = "https://comicvine.gamespot.com/api/issue/4000-{}/?api_key={}&field_list=location_credits,character_credits,team_credits,image&format=json"
