import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request


load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")
base_url = "https://api.steampowered.com"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

    #return jsonify({"message": "Hii its flask api"})

@app.route("/submit", methods=["POST"])
def submit():
    form_count = int(request.form.get("UsersNum",1))
    return render_template("InputGraph.html", users=form_count)

@app.route("/UsersSubmit", methods=["POST"])
def UsersSubmit():
    answers = []
    class User_Contribution:
            def __init__(self, username, game_num):
                self.username = username
                self.game_num = game_num
    famshare_taken = request.form.get("famshare")
    chosen_comparison = request.form.get("comparison-type")
    if famshare_taken:
        famshare_answer = True
    else:
        famshare_answer = False

    for key in request.form:
        if key.startswith("SteamID_"):
            steam_id = request.form.get(key)
            if steam_id:
        #Steam_id = request.form.get("SteamID")
                print(chosen_comparison,"MMMMM")
                if chosen_comparison == "value":
                    Total_games = get_user_games(steam_id,famshare_answer,chosen_comparison)
                    total_value = 0
                    for game in Total_games:
                        app_id = str(game["appid"])
                        price = get_game_price(app_id)
                        print(price)
                        if price is not None:
                            total_value += price
                    Username = get_username(steam_id)
                    CurrentUser = User_Contribution(Username,total_value)
                elif chosen_comparison == "game-count":
                    Total_games = get_user_games(steam_id,famshare_answer,chosen_comparison)
                    #if famshare_answer:
                        #Total_games = game_list_filter(appid_games)
                    Username = get_username(steam_id)
                    game_count = len(Total_games)
                    CurrentUser = User_Contribution(Username,game_count)
                answers.append(CurrentUser)
                #answers.append(f"{Username}: {game_count} games")
                
    usernames_list = []
    total_games_list = []
    for user in answers:
        usernames_list.append(user.username)
    for games in answers:
        total_games_list.append(games.game_num)
    #print(usernames_list)
    #print(total_games_list)
    print("HEYYYYYY HERERERERRERERERE")
    #taken_answers = "<br>".join(answers)
    #print(answers)
    return render_template("UsersSubmit.html",usernames_list=usernames_list,total_games_list=total_games_list)
    #print(get_user_games(Steam_id))


def get_user_games(steam_id,famshare,comparison_type):
    url = f"{base_url}/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
    response = requests.get(url)
    Games_name_list = []
    if response.status_code == 200:
        print("User game library retrieved")
        user_games_data = response.json()
        response_data = user_games_data.get("response", {})
        games_list = response_data.get("games", [])
        #gamesid_list = response_data.get("appid", [])
        for game in games_list:
            if comparison_type == "value":
                if famshare:
                    if game_is_famshare(game["appid"]):
                        Games_name_list.append({"name": game["name"], "appid": game["appid"]})
                else:
                    Games_name_list.append({"name": game["name"], "appid": game["appid"]})
            else:
                if famshare:
                    if game_is_famshare(game["appid"]):
                        Games_name_list.append({"name": game["name"], "appid": game["appid"]})
                else:
                    Games_name_list.append({"name": game["name"], "appid": game["appid"]})
        return Games_name_list
    else:
        print("Failed to retrieve user game library")

def game_is_famshare(app_id):
    app_id = str(app_id)
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&filters=categories"
    response = requests.get(url)
    if response.status_code == 200:
        print("Game if uhh is fam share retrieved")
        game_data = response.json()
        if isinstance(game_data, dict):
            if app_id in game_data:
                if game_data[app_id].get("success"):
                    if "categories" in game_data[app_id]["data"]:      
                        cat_len = len(game_data[app_id]["data"]["categories"])
                        for cat in range(cat_len):
                            cat_row = str(game_data[app_id]["data"]["categories"][cat])
                            if cat_row[7:9] == "62":
                                print("HAS FAMILY SHARE")
                                return True
                        print("No family share...")
                        return False

def get_game_price(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&filters=price_overview&cc=ae"
    response = requests.get(url)
    if response.status_code == 200:
        print("Game price retrieved")
        game_data = response.json()
        if isinstance(game_data, dict):
            if app_id in game_data:
                if game_data[app_id].get("success"):
                    if "price_overview" in game_data[app_id]["data"]:
                        price_info = game_data[app_id]["data"]["price_overview"]
                        if price_info["discount_percent"] == 0:
                            final_price = price_info.get("final", 0) / 100.0
                        else:
                            final_price = price_info.get("initial", 0) / 100.0
                        return final_price
                    else:
                        print("Price unavailable")
                        return None
                else:
                    print("Failed to get the game details")
                    return None
            else:
                print("no app id data")
                return None
        else:
            print("Unable to get the game data")
            return None
    else:
        print("Failed to even retrieve the data")
        return None

def game_list_filter(game_list):
    new_game_list = []
    for game_id in game_list:
        if game_is_famshare(game_id):
            new_game_list.append(game_id)
    return new_game_list

def get_username(steam_id):
    url = f"{base_url}/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={steam_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print("User name retrieved")
        user_name_data = response.json()
        response_data = user_name_data.get("response", {})
        players_list = response_data.get("players", [])
        username = players_list[0].get("personaname")
        return f"User: {username}"


#app_id = input("enter app id: ")
#game_is_famshare(app_id)

#Steam_id = input("Enter your Steam ID: ")
#User_games_data = get_user_games(Steam_id)
#response_data = User_games_data.get("response", {})
#games_list = response_data.get("games", [])

#for game in games_list:
#    print(game["name"])
#print(f"Total games: {len(games_list)}")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #debug=True)