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
    for key in request.form:
        if key.startswith("SteamID_"):
            steam_id = request.form.get(key)
            if steam_id:

        #Steam_id = request.form.get("SteamID")
                Total_games = get_user_games(steam_id)
                Username = get_username(steam_id)
                game_count = len(Total_games)
                answers.append(f"{Username}: {game_count} games")
    return "<br>".join(answers)
    #print(get_user_games(Steam_id))


def get_user_games(steam_id):
    url = f"{base_url}/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
    response = requests.get(url)
    Games_name_list = []
    if response.status_code == 200:
        print("User game library retrieved")
        user_games_data = response.json()
        response_data = user_games_data.get("response", {})
        games_list = response_data.get("games", [])
        for game in games_list:
            Games_name_list.append(game["name"])
        return Games_name_list
    else:
        print("Failed to retrieve user game library")

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

#Steam_id = input("Enter your Steam ID: ")
#User_games_data = get_user_games(Steam_id)
#response_data = User_games_data.get("response", {})
#games_list = response_data.get("games", [])

#for game in games_list:
#    print(game["name"])
#print(f"Total games: {len(games_list)}")


if __name__ == "__main__":
    app.run(debug=True)