from tkinter import *
from BlokusPlayer import BlokusPlayer
from BlokusGridFrame import BlokusGridFrame
import time
import threading
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

# START THE GAME

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
turn_thread = threading.Thread(target=turn_loop, daemon=True)
turn_thread.start()

window.mainloop()