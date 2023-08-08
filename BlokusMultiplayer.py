import firebase
import requests
import sys
import secrets
import string
from tkinter import *

import BlokusBoard
from BlokusPlayer import BlokusPlayer
from BlokusGridFrame import BlokusGridFrame
import time
import threading

# eml = input("Email:")
# pwd = input("Password:")
eml = 'jjreder@gmail.com'
pwd = 'securePassword!@#$'
config = {"apiKey": "AIzaSyDg3Dpset2DrpWn-8Ci3C1PyIl_y1ws9aw",
  "authDomain": "blokuscloud.firebaseapp.com",
  'databaseURL': 'blokuscloud.firebaseio.com',
  "projectId": "blokuscloud",
  "storageBucket": "blokuscloud.appspot.com",
  "messagingSenderId": "184635241096",
  "appId": "1:184635241096:web:17e23ac067c4a9a4a9653d"}

app = firebase.initialize_app(config)
auth = app.auth()
user = auth.sign_in_with_email_and_password(eml, pwd)
print(user)
print("You are signed in!")
db = app.firestore()
games = db.collection('games')
window = Tk(className="BlokusGUI")
window.title("BlokusGUI")
window.configure(height=500, width=500)
FONT = 'Courier New'
current_turn_label = Label(window, font=(FONT, 20))
current_turn_label.place(x=250, y=100, anchor='center')
# game var
blokus_grid_frame = BlokusGridFrame(window, 250, 300, 300, 300)
PLAYERS_NUM = 2
COLORS = [1, 2, 3, 4]
FRIENDLY_NAMES = ['Red', 'Blue', 'Yellow', 'Green']
PLAYERS = [BlokusPlayer(blokus_grid_frame, COLORS[i]) for i in range(PLAYERS_NUM)]
TURN = 0
HAS_PLAYED = False
def turn_loop():
    global TURN
    global PLAYERS
    global COLORS
    global HAS_PLAYED
    while True:
        player = PLAYERS[TURN]
        if player.can_play:
            player.can_play = blokus_grid_frame.board.can_play(player.pieces, COLORS[TURN], player.first_move)
            print("VALID MOVES", len(player.can_play))
        if not player.can_play:

            continue_game = False
            for player_person in PLAYERS:
                if player_person.can_play:
                    continue_game = True
                    break
            print(continue_game)
            if continue_game:
                TURN += 1
                TURN %= PLAYERS_NUM
                continue
            else:
                print("Game over!")
                current_turn_label.config("Game Over!")
        current_turn_label.config(text="It\'s "+FRIENDLY_NAMES[TURN]+"\'s turn! ("+str(len(player.can_play))+" moves)")
        player.get_and_play_move()
        while not player.signal:
            time.sleep(0.2)
        TURN += 1
        TURN %= PLAYERS_NUM


def concatenate(list_of_dict):
    return_dict = {}
    for dic in list_of_dict:
        return_dict.update({list(dic.keys())[0]: list(dic.values())[0]})
    return return_dict


def board_string_to_blokus_board(bs):
    return BlokusBoard.BlokusBoard([[int(j) for j in i] for i in bs])

def get_game_data(game_id):
    games._path = ['games']
    game_data = concatenate(games.get(user['idToken']))
    return game_data[game_id]


def update_game_data(new_game_data, game_id):
    doc = games.document(game_id)
    for key in new_game_data.keys():
        doc._path = ['games', game_id]
        doc.update({key: new_game_data[key]}, user['idToken'])

def join_game(game_id):
    """
    Join a game.
    :param game_id: The game id of the game to join
    :return:
    """
    dt = get_game_data(game_id)
    if not dt['in_lobby']:
        print("Spectator mode has not been implemented.")
        return
    if dt['max_players'] <= len(dt['players']):
        print("Spectator mode has not been implemented.")
        return
    if user['localId'] in dt['players']:
        print("Rejoining game...")
    else:
        if dt['op'] == '':
            print("Claiming OP...")
            dt['op'] = user['localId']
        dt['players'].append(user['localId'])
        dt['current_players'] += 1
        update_game_data(dt, game_id)


what2do = input("[1] Create game\n[2] Join game\n:")
if what2do == '1':
    game_id = games.add({'board': ["0"*20 for j in range(20)], 'in_lobby': True, 'max_players': 4,
                         'current_players': 0, 'players': ['testing'], 'op': ''}, user['idToken'])
    print("Your game has been created! ID:", game_id)
    print("Joining game...")
    join_game(game_id)
if what2do == '2':
    game_id = input("Enter the game that you want to join: ").replace('\n', '').replace(' ', '')
    join_game(game_id)