# Import Required Libraries
from flask import (Flask, render_template, request, redirect, url_for, flash, jsonify)
from flask import session as loginSession, make_response
import json
import requests


app = Flask(__name__)
Application_Name = "Sports Roster App"


# Establish Connection to API Source
t = requests.get('https://www.balldontlie.io/api/v1/teams')
teamData = t.json()

p = requests.get('https://www.balldontlie.io/api/v1/players')
playerData = p.json()


# Assist Functions
def teamList():
    list_team = []
    for i in teamData['data']:
        list_team.append(i['full_name'])
    return list_team

def playerList(teamName):
    onRoster = []
    for p in playerData['data']:
        if p['team']['full_name'] == teamName:
            onRoster.append(p)


# App Routes
# Method for Displaying Home and Team Nav Menu
@app.route('/')
def teamMenu():
    return render_template('index.html', teams=teamList())

# Method for Displaying Selected Team's Roster
@app.route('/show/<teamName>')
def playerList(teamName):
    onRoster = []
    for p in playerData['data']:
        if p['team']['full_name'] == teamName:
            onRoster.append(p)
    return render_template('show.html', teams=teamList(), players=onRoster, currentTeam=teamName)


if __name__ == '__main__':
    app.run()
