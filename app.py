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

@app.route("/submit", methods=["GET"])
def submit():
    Steam_id = request.args.get("SteamID")
    Total_games = get_user_games(Steam_id)
    return Total_games
    #print(get_user_games(Steam_id))


def get_user_games(steam_id):
    url = f"{base_url}/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
    response = requests.get(url)
    Games_list = []
    if response.status_code == 200:
        print("User game library retrieved")
        user_games_data = response.json()
        response_data = user_games_data.get("response", {})
        response_games_list = response_data.get("games", [])
        for game in response_games_list:
            Games_list.append(game["name"])
        return Games_list
    else:
        print("Failed to retrieve user game library")

#Steam_id = input("Enter your Steam ID: ")
#User_games_data = get_user_games(Steam_id)
#response_data = User_games_data.get("response", {})
#games_list = response_data.get("games", [])

#for game in games_list:
#    print(game["name"])
#print(f"Total games: {len(games_list)}")


if __name__ == "__main__":
    app.run(debug=True)