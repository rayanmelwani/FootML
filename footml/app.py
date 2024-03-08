from flask import Flask, render_template, request, jsonify, make_response, redirect
import numpy as np
from numpy.random import default_rng
import pandas as pd
import csv
import time
import schedule
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import runtoAPI_final as api_call
import rnn

footml = Flask(__name__)

PLAYERS_PER_TEAM = 15
MAX_PLAYERS_PER_CLUB = 3
MAX_ROLES = {'GK': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}
GAMEWEEK = 38


def update_predicted_points():
    api_call.update_data()
    predictions = rnn.train_and_predict()
    df = pd.read_csv("database/cleaned_simple_database_21_22")
    drop = ["pred_points"]
    df = df.drop(drop, axis = 1)
    updated_df = pd.merge(df, predictions, on="name")
    updated_df.to_csv("database/cleaned_simple_database_21_22")

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_predicted_points, trigger="interval", days=7, start_date='2022-08-02 09:00:00')
scheduler.start()

#This function creates a pandas dataframe with all the player information
def open_df():
    seed=1000
    data = pd.read_csv('footml/database/cleaned_simple_database_21_22.csv', ',')
    data = data.iloc[:1355,]
    return data

#Function to get current gameweek from updated csv
def get_gameweek():
    return GAMEWEEK

#This function finds the top players for every function
def find_top_players(top_players):
    data = open_df()
    gk = data.loc[data['element_type']=='GK']
    gk = gk.sort_values(by=['pred_points'],ascending=False)
    defender = data.loc[data['element_type']=='DEF']
    defender = defender.sort_values(by=['pred_points'],ascending=False)
    mid = data.loc[data['element_type']=='MID']
    mid = mid.sort_values(by=['pred_points'],ascending=False)
    fwd = data.loc[data['element_type']=='FWD']
    fwd = fwd.sort_values(by=['pred_points'],ascending=False)

    for i in range(3):
        temp = [gk.iloc[i]['Team'], gk.iloc[i]['Name'], gk.iloc[i]['now_cost'], gk.iloc[i]['pred_points']]
        top_players.append(temp)

    for i in range(5):
        temp = [defender.iloc[i]['Team'], defender.iloc[i]['Name'], defender.iloc[i]['now_cost'], defender.iloc[i]['pred_points']]
        top_players.append(temp)

    for i in range(5):
        temp = [mid.iloc[i]['Team'], mid.iloc[i]['Name'], mid.iloc[i]['now_cost'], mid.iloc[i]['pred_points']]
        top_players.append(temp)

    for i in range(3):
        temp = [fwd.iloc[i]['Team'], fwd.iloc[i]['Name'], fwd.iloc[i]['now_cost'], fwd.iloc[i]['pred_points']]
        top_players.append(temp)

    return None

#This function checks if a typed in name matches a fullname string
def name_match(inputname, fullname):
    input = inputname.upper().replace(' ','')
    full = fullname.upper().replace(' ', '')
    return (input in full)

def gen_players():
    player_data = []
    with open("footml/database/cleaned_simple_database_21_22.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            second_name = row["second_name"]
            cleaned = name.replace(' ','')
            cleaned = cleaned.replace('-','')
            cleaned = cleaned.replace('\'','')
            player_data.append([name,cleaned, second_name]) #second_name just for sorting by surname
    player_data.sort(key=lambda y: y[2])
    for datapoint in player_data:
        datapoint = datapoint[:-1] #do not return second_name
    return player_data

def gen_full_player_data():
    player_data = []
    with open("footml/database/cleaned_simple_database_21_22.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            elementName = name.replace(' ','')
            elementName = elementName.replace('-','')
            elementName = elementName.replace('\'','')
            role = row["element_type"]
            cost = row["now_cost"]
            team = row["Team"]
            points = float(row["pred_points"])

            player_data.append([name, elementName, role, cost, team, points]) #second_name just for sorting by surname
    player_data.sort(key=lambda y: y[-1], reverse=True)
    datadata = []
    for datapoint in player_data:
        datadict = {"name": datapoint[0],
                    "elementName": datapoint[1],
                    "role": datapoint[2],
                    "cost": datapoint[3],
                    "team": datapoint[4],
                    "points": datapoint[5]}
        datadata.append(datadict)
    return datadata

#return the dictionary corresponding to the highest scoring player for this next gameweek
def get_best_player():
    player_data = gen_full_player_data()
    best_player = player_data[0]
    return best_player

#didn't end up being implemented due to end of season
def get_schedule(team_name):
    schedule = {}
    schedule = ""
    return schedule

#return the information in the database about the player
def get_player_info(player_name):
    data = open_df()
    player = data.loc[data["Name"]==player_name]
    player_info = {"name": player_name, "team": player.iloc[0]["Team"], \
        "role": player.iloc[0]["element_type"], "cost": player.iloc[0]["now_cost"], "points": player.iloc[0]["pred_points"]}
    player_info.update({"schedule": get_schedule(player_name)})
    return player_info

#class used to generate transfers and ensure that teams submitted by users
#satisfy the constraints of FPL.
class Team:
    def __init__(self, players):
        self.players = players
        self.roles = {'GK': 0, 'DEF': 0, 'MID': 0, 'FWD': 0} #how many players in each role
        self.represented_clubs = {}
        self.team_value = 0
        self.extra_funds = 0
        # Add player roles
        if players:
            for player in self.players:
                for role in self.roles:
                    if player["element_type"] == role:
                        self.roles[role] += 1
            # Add player clubs
            for player in self.players:
                if player["Team"] not in self.represented_clubs.keys():
                    self.represented_clubs[player["Team"]] = 0
                self.represented_clubs[player["Team"]] += 1
            # Add total team value
            value = 0
            for player in self.players:
                value += float(player["now_cost"])
            self.team_value = value

    # Function that checks whether team meets constraints
    def constraint_checks(self):

        #Check for correct number of players
        '''I've taken this out for now cos I don't think we should be making
        sure user has plugged in 15 players '''
        #if len(self.players) != PLAYERS_PER_TEAM:
            #return False

        #Check that there is a max of three players per premier league team
        if any(count > MAX_PLAYERS_PER_CLUB for count in self.represented_clubs.values()):
            return 1

        #Check that roles have been successfully allocated
        for role in self.roles:
            if self.roles[role] > MAX_ROLES[role]:
                return 2

        return 0

    # Function that sets extra funds for team
    def set_funds(self, funds):
        self.extra_funds = funds

    # Helper function for transfer recommendation
    def eval_transfer(self):
        #Check that there is a max of three players per premier league team

        if any(count > MAX_PLAYERS_PER_CLUB for count in self.represented_clubs.values()):
            return False
        #Check that roles have been successfully allocated

        for role in self.roles:
            if self.roles[role] > MAX_ROLES[role]:
                return False
        #Checking extra_funds constraint

        if self.extra_funds < 0:
            return False
        return True

    #Function that adds a player to the team.players list
    def add_player(self, player):
        #add player
        self.players.append(player)
        #update roles
        for role in self.roles:
            if player["element_type"] == role:
                self.roles[role] += 1
        #update teams
        if player["Team"] not in self.represented_clubs.keys():
            self.represented_clubs[player["Team"]] = 0
        self.represented_clubs[player["Team"]] += 1
        #update team value & extra funds
        self.team_value += float(player["now_cost"])
        self.extra_funds -= float(player["now_cost"])

    #Function to remove specified player from player list
    def remove_player(self,name):
        #searched through players
        for i,player in enumerate(self.players):
            #if matching name
            if player["Name"]==name:
                #decrements role
                self.roles[player["element_type"]] -= 1
                #decrements team counter
                self.represented_clubs[player["Team"]] -= 1
                #decrements team value and updates extra funds
                self.team_value -= float(player["now_cost"])
                self.extra_funds += float(player["now_cost"])
                #removes player
                self.players.pop(i)
                break


    #Function that returns total points of team
    def calculate_points(self):
        total = 0
        for player in self.players:
            total += float(player["pred_points"])
        return total

#Function that finds the optimal transfer (bottom-up dynamic programming)
def find_optimal_transfer(team):
    df = open_df()
    df = df.reset_index()
    maxpoints = team.calculate_points()
    transferin = {}
    transferout = {}




    #iterating over all players in the team
    for player in team.players:
        #removes player
        removedplayer = player
        team_copy = Team(list(team.players))
        team_copy.set_funds(team.extra_funds)
        team_copy.remove_player(removedplayer["Name"])


        #iterating over all players in df
        attributes = ["Name", "now_cost", "element_type", "pred_points", "first_name", "second_name", "Team"]
        for index,row in df.iterrows():
            #checks if player in team already
            inteam = 0
            if removedplayer["Name"] == row["Name"]:
                inteam = 1
            for player in team_copy.players:
                if row["Name"]==player["Name"]:
                    inteam = 1
            if inteam == 0:
                #creates player dictionary if position match
                player_dict = {}
                if row["element_type"] == removedplayer["element_type"]:
                    for i in attributes:
                        player_dict[i] = row[i]
                    #alternative: playerdict = df.iloc[index].to_dict()
                    #add player

                    team_copy.add_player(player_dict)
                    #if passes constraints
                    if team_copy.eval_transfer():
                        #if increases max points, save transfer
                        if team_copy.calculate_points() > maxpoints:
                            maxpoints = team_copy.calculate_points()
                            transferin = player_dict
                            transferout = removedplayer
                    team_copy.remove_player(player_dict["Name"])

    if maxpoints == team.calculate_points():
        return ["Null", "Null"]

    return [transferin, transferout]

#Function that recommends 3 transfers, returns a dictionary of transfers {playerout:playerin}
def build_transferlist(team):

    transferlist = {}
    transfer = find_optimal_transfer(team)

    #if no proposed transfers, set dictionary values to None
    if len(temp) == 0:
        transferlist["transfer_in"] = None
        transferlist["transfer_out"] = None
    #otherwise, set dict values to proposed transfers
    else:
        transferlist["transfer_in"] = transfer[0]
        transferlist["transfer_out"] = transfer[1]
    #returns transferlist

    return transferlist

#----------------Landing Pages----------------#

@footml.route("/")
def index():
    return render_template("welcome.html")

#----------------Navigation bar at the top----------------#

@footml.route("/how-it-works", methods=["POST", "GET"])
def howitworks():
    return render_template("how-it-works.html", gameweek=get_gameweek())

@footml.route("/team-selection", methods=["GET", "POST"])
def teamselection():
    player_data = gen_players()
    return render_template("home_page.html", data=player_data)

@footml.route("/predict_transfers", methods=["POST"])
def predict_transfers():
    data = request.get_json()
    team = data["players"]
    funds = float(data["funds"])
    team = Team(team)
    team.set_funds(funds)
    df = open_df()
    transfers = find_optimal_transfer(team)
    transferJSON = {"transferin": transfers[0], "transferout": transfers[1]}
    return make_response(jsonify(transferJSON), 200)

@footml.route("/recommendation", methods =["GET", "POST"])
def register():
    return render_template("return_team.html")

@footml.route("/top-performers", methods=["POST"])
def topperformers():
    top_players = []
    find_top_players(top_players)
    player_names = gen_players()
    return render_template("top-performers.html", top_players = top_players, data=player_names, gameweek=get_gameweek())

@footml.route("/player-search", methods=["GET", "POST"])
def player_search():
    return render_template("player-search.html")


#----------------Navigation bar at the bottom----------------#

@footml.route("/about-us", methods=["POST"])
def aboutus():
    return render_template("about-us.html")

@footml.route("/contact", methods=["POST"])
def contact():
    return render_template("contact-us.html")

@footml.route("/privacy-policy", methods=["POST"])
def privpol():
    return render_template("privacy-policy.html")

#----------------JSON Methods----------------#

@footml.route('/json', methods=["POST"])
def json():
    team = request.get_json()
    current_players = team.get("current_players")
    new_player = team.get("new_player")
    new_player_dict = {}

    exists = 0
    with open("footml/database/cleaned_simple_database_21_22.csv", "r",encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if name_match(new_player, row["Name"]):
                player_dict = row
                for current_player in current_players:
                    if current_player["Name"] == player_dict["Name"]:
                        json_response = {"message": "failure_alreadyinteam"}
                        res = make_response(jsonify(json_response), 200)
                        return res
                current_players.append(player_dict)
                new_player_dict = player_dict
                exists = 1
                break

    if exists==0:
        json_response = {"message": "failure_doesnotexist"}
        res = make_response(jsonify(json_response), 200)

    team_obj = Team(current_players)
    checks = team_obj.constraint_checks()

    if new_player_dict:
        if '\'' in new_player_dict['Name']:
            new_player_dict['Name'] = new_player_dict['Name'].replace('\'','')

    if checks==0 and new_player_dict:
        if new_player_dict.get(""):
            new_player_dict.pop("")
        json_response = {"message": "success", "new_player": new_player_dict}
        res = make_response(jsonify(json_response), 200)
        return res
    elif checks==1:
        json_response = {"message": "failure_maxplayersperclub"}
        res = make_response(jsonify(json_response), 200)
        return res
    elif checks==2:
        json_response = {"message": "failure_maxrolesperteam"}
        res = make_response(jsonify(json_response), 200)
        return res
    else:
        json_response = {"message": "failure"}
        res = make_response(jsonify(json_response), 200)
        return res


@footml.route('/player-info', methods=["POST"])
def player_info():
    player = request.get_json()
    player_name = player.get("name")
    gameweek = get_gameweek()
    info = {"info": get_player_info(player_name), "gameweek": str(gameweek)}
    res = make_response(jsonify(info), 200)
    return res

@footml.route('/best-player', methods=['POST'])
def best_player():
    best_player = get_best_player()
    info = {"best_player": best_player}
    res = make_response(jsonify(info), 200)
    return res


@footml.route('/player-search-list', methods=["POST"])
def player_search_list():
    player_data = gen_full_player_data()
    res = make_response(jsonify(player_data), 200)
    return res
