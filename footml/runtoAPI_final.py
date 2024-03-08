import pandas as pd
import numpy as np
import requests
#from tqdm.auto import tqdm
#tqdm.pandas()

def update_data():

    # base url for all FPL API endpoints
    base_url = 'https://fantasy.premierleague.com/api/'

    # get data from bootstrap-static endpoint
    r = requests.get(base_url+'bootstrap-static/').json()

    # show the top level fields

    players = pd.json_normalize(r['elements'])

    drop = [ 'chance_of_playing_next_round', 'chance_of_playing_this_round', 'code',
           'cost_change_event', 'cost_change_event_fall', 'cost_change_start',
           'cost_change_start_fall', 'dreamteam_count', 'element_type', 'ep_next',
           'ep_this', 'event_points', 'form', 'in_dreamteam',
           'news', 'news_added', 'now_cost', 'photo', 'points_per_game',
           'selected_by_percent', 'special', 'squad_number',
           'status', 'team', 'team_code', 'total_points', 'transfers_in',
           'transfers_in_event', 'transfers_out', 'transfers_out_event',
           'value_form', 'value_season', 'web_name', 'minutes', 'goals_scored',
           'assists', 'clean_sheets', 'goals_conceded', 'own_goals',
           'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards',
           'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat',
           'ict_index', 'influence_rank', 'influence_rank_type', 'creativity_rank',
           'creativity_rank_type', 'threat_rank', 'threat_rank_type',
           'ict_index_rank', 'ict_index_rank_type',
           'corners_and_indirect_freekicks_order',
           'corners_and_indirect_freekicks_text', 'direct_freekicks_order',
           'direct_freekicks_text', 'penalties_order', 'penalties_text']
    players = players.drop(drop,axis=1)

    g = requests.get('https://fantasy.premierleague.com/api/event/36/live/').json()


    gw = pd.json_normalize(g['elements'])

    gw = gw.drop('explain', axis = 1)

    df = pd.merge(
        left=players,
        right=gw,
        on='id'
    )

    drop = ['id', 'stats.minutes',
           'stats.goals_scored', 'stats.assists', 'stats.clean_sheets',
           'stats.goals_conceded', 'stats.own_goals', 'stats.penalties_saved',
           'stats.penalties_missed', 'stats.yellow_cards', 'stats.red_cards',
           'stats.saves', 'stats.bonus', 'stats.bps', 'stats.influence',
           'stats.creativity', 'stats.threat', 'stats.ict_index',
            'stats.in_dreamteam']

    df = df.drop(drop,axis=1)

    # print(df)

    alldata = pd.read_csv("database/completed_data_gw.csv")
    df['GW_Adjusted'] = alldata.GW_Adjusted.max()+1
    df['name'] = df['first_name'] + " " + df['second_name']

    drop = ['first_name', 'second_name']
    df = df.drop(drop, axis=1)
    print(df)

    df.rename(columns={'stats.total_points':'total_points'}, inplace=True)

    frames = [alldata, df]

    result = pd.concat(frames)
    print(result)

    result.to_csv('database/completed_data_gw.csv')
