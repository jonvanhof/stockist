import stockist
from flask import Flask
from flask_cors import CORS

stk = stockist.Stockist('demo')

mlb_teams_fields = {'seas_team_id': 'string pk',
                    'season': 'string',
                    'name': 'string',
                    'league': 'string',
                    'city': 'string',
                    'ballpark': 'string'}
stk.add_object('team', mlb_teams_fields, 0)

stk.add_source('mlb', 'json', "http://lookup-service-prod.mlb.com/json/named.")

query_path = "team_all_season.bam?sport_code='mlb'&all_star_sw='N'"


def qry_func(res_dict):
    ret_rows = []
    for i in res_dict['team_all_season']['queryResults']['row']:
        ret_dict = {'seas_team_id': i['mlb_org_id'] + "." + i['season'],
                    'season': i['season'],
                    'name': i['name_display_long'],
                    'league': i['league'],
                    'city': i['city'] + ", " + i['state'],
                    'ballpark': i['venue_name']}
        ret_rows.append(ret_dict)
    return ret_rows


stk.add_stock_request(stk.sources[0], stk.objects[0], query_path, qry_func)
params = {"season": "2019"}
stk.stock_requests[0].stock(params)
params = {"season": "1999"}
stk.stock_requests[0].stock(params)

stk.add_endpoint("teams", stk.objects[0], ['season'])

stk_app = Flask(__name__)
CORS(stk_app)
stk.create_endpoints(stk_app)
