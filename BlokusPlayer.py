import pieces
from BlokusGridFrame import BlokusGridFrame
from BlokusPiece import  BlokusPiece
class BlokusPlayer:
    def __init__(self, bgf: BlokusGridFrame, color: int, move_determine_function=None) -> None:
        self.pieces = pieces.return_pieces()
        self.bgf = bgf
        self.color = color
        self.first_move = True
        self.signal = False
        self.can_play = True
        self.ai_func = move_determine_function # a function that takes color id and BlokusBoard and pieces to return move
    def played_hook(self, pid):
        self.signal = True
        self.pieces.pop(pid)
    def get_and_play_move(self):
        self.signal = False
        if self.ai_func is not None:
            move = self.ai_func(self.color, self.bgf.board, self.pieces) # (piece_id, move-x, move-y)
            self.bgf.update_current_pieces(self.pieces[move[0]], self.color, self.first_move)
            self.first_move = False
            self.bgf.mouse_coords = (move[1], move[2])
            self.bgf.play()
            self.pieces.pop(move[0])
        else:
            self.bgf.update_current_pieces(self.pieces, self.color, self.first_move, played_hook=self.played_hook)
            self.bgf.enable_hover_mode()
            self.bgf.played_hook = self.played_hook
            self.first_move = False

      

# import tkinter, threading, time
# w = tkinter.Tk()
# w.configure(height=500, width=500)
# b = BlokusGridFrame(w, 250, 250, 500, 500, False) 

# def turn_loop():
#     player_1 = BlokusPlayer(b, 2)
#     player_2 = BlokusPlayer(b, 3)
#     players = [player_1, player_2]
#     turn = 0
#     while True:
#         print('next')
#         print(players[turn].bgf.board.can_play(players[turn].pieces, players[turn].color, players[turn].first_move))
#         players[turn].get_and_play_move()
#         while not players[turn].signal:
#             time.sleep(0.2)
#             continue
#         turn += 1
#         turn %= len(players)
# t = threading.Thread(target=turn_loop)
# t.start()
# w.mainloop()