# Import Required Libraries
from flask import (Flask, render_template, request, redirect, url_for, flash, jsonify)
from flask import session as loginSession, make_response
import json
import requests


app = Flask(__name__)
Application_Name = "Sports Roster App"


###### Establish Connection to API Source
# Get Team API data
t = requests.get('https://www.balldontlie.io/api/v1/teams')
teamData = t.json()

# Get Player API data
def getPlayerData():
    playerResults = []
    try:
        for pg_num in range(1, 33):
            url = "https://www.balldontlie.io/api/v1/players?per_page=100&page=" + str(pg_num)
            r = requests.get(url)
            r_json = r.json()
            playerResults = playerResults + r_json['data']
        return playerResults
    except Exception as e:
        print("This is a Player Data error!")


###### Assist Functions
# Placeholder for returned player API data
playerData = getPlayerData()

# Filter team API data for navbar
def teamList():
    try:
        list_team = []
        for i in teamData['data']:
            list_team.append(i['full_name'])
        return list_team
    except Exception as e:
        print("This is a Team Data error!")


###### App Routes
# Method for Displaying Homepage and Team Nav Menu
@app.route('/')
def teamMenu():
    return render_template('index.html', teams=teamList())

# Method for Displaying Selected Team's Roster
@app.route('/show/<teamName>')
def playerList(teamName):
    getRoster = playerData
    onRoster = []
    for p in range(len(getRoster)):
        if getRoster[p]['team']['full_name'] == teamName:
            onRoster.append(getRoster[p])
            if len(onRoster) == 18:
                break
    return render_template('show.html', teams=teamList(), players=onRoster, currentTeam=teamName)


if __name__ == '__main__':
    app.run()
