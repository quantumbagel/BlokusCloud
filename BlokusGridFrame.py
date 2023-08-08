import tkinter
import pieces
from BlokusBoard import BlokusBoard
from BlokusPiece import BlokusPiece
class BlokusGridFrame(tkinter.Frame):
    def __init__(self, container, x, y, h, w, enable_motion=False, overload_board=None):
        super().__init__(container)
        self.verbosity = 0 # 0: none, 1: errors, 2: all
        self.verbose_messages = ['no output / fatal', 'errors / warnings only', 'all']
        self.verbose_levels = ['FATAL', ' WARN', ' INFO']
        print("VERBOSITY:", self.verbosity, '('+self.verbose_messages[self.verbosity]+')')
        
        self.grid = [[('gray75', 'black') for i in range(20)] for j in range(20)]
        self.container: tkinter.Tk = container  
        self.frame=tkinter.Frame(self.container, background="white", highlightbackground="red", highlightthickness=1, height=h, width=w)
        self.frame.place(x=x, y=y, anchor='center')
        self.canvas = tkinter.Canvas(self.frame, width=w, height=h, background='gray75')
        self.canvas.place(x=w/2, y=h/2, anchor='center')
        self.draw_rectangles(w, h)
        if overload_board is not None:
            self.board = overload_board
        else:
            self.board = BlokusBoard()
        self.mouse_coords = (0,0)
        self.height = h
        self.width = w
        self.enable_motion = enable_motion
        self.current_pieces = []
        self.piece_colors = ['gray75', 'red', 'blue', 'yellow', 'green']
        self.piece_color = 0
        self.current_selected_piece = 0
        self.hover_outline_good = 'green'
        self.hover_outline_bad = '#8B0000' # dark red
        self.current_piece_firstmove = False
        self.show_board = [[('gray75', 'black', 1) for i in range(20)] for j in range(20)]
        self.last_move = (None, None, None)
        self.canvas.focus() # focus 
        self.mouse_over = False
        self.played_hook = lambda: None
        if self.enable_motion:
            self.enable_hover_mode()
        # Create rectangles on whole window
    def update_current_pieces(self, piece_s, color, firstmove=False, played_hook=lambda: None):
        self.piece_color = color
        self.current_pieces = piece_s
        self.current_selected_piece = 0
        self.current_piece = BlokusPiece(piece_s[0], self.piece_color)
        self.current_piece_firstmove = firstmove
        self.played_hook = played_hook
        self.mirror_showgrid()

    def next_piece(self):
        self.vprint("BlokusGridFrame.next_piece: going to next piece", 2)
        self.current_selected_piece += 1
        self.current_selected_piece %= len(self.current_pieces)
        self.current_piece = BlokusPiece(self.current_pieces[self.current_selected_piece], self.piece_color)
        self.mirror_showgrid()

    def previous_piece(self):
        self.current_selected_piece -= 1
        self.current_selected_piece %= len(self.current_pieces)
        self.current_piece = BlokusPiece(self.current_pieces[self.current_selected_piece], self.piece_color)
        self.mirror_showgrid()

    def mouse_over_handler(self, event):
        self.vprint("BlokusGridFrame.mouse_on_handler: mouse has arrived", 2)
        self.mouse_over = True

    def mouse_off_handler(self, event):
        self.vprint("BlokusGridFrame.mouse_off_handler: mouse has left", 2)
        self.mouse_over = False

    def draw_rectangles(self, w, h):
        self.canvas.delete('all')
        c = 0
        for x in range(0, w, int(w/20)):
            for y in range(0, h, int(h/20)):
                c += 1
                box = (x, y, x + w/20, y + h/20)
                self.canvas.create_rectangle(box, fill=self.grid[y//int(h/20)][x//int(w/20)][0], outline=self.grid[y//int(h/20)][x//int(w/20)][1])

    def fixed_bind(self, binding, func):
        self.bind_all(binding, func)

    def fixed_unbind(self, binding):
        self.unbind_all(binding)
    def rotate_cw(self):
        self.vprint("BlokusGridFrame.rotate_cw: rotating cw", 2)
        self.current_piece.rotate_cw()
        self.mirror_showgrid()
    def rotate_ccw(self):
        self.vprint("BlokusGridFrame.rotate_ccw: rotating ccw", 2)
        self.current_piece.rotate_ccw()
        self.mirror_showgrid()
    def reflect_x(self):
        self.vprint("BlokusGridFrame.reflect_x: reflecting across x-axis", 2)
        self.current_piece.reflect_x()
        self.mirror_showgrid()
    def reflect_y(self):
        self.vprint("BlokusGridFrame.reflect_y: reflecting across y-axis", 2)
        self.current_piece.reflect_y()
        self.mirror_showgrid()
    def enable_hover_mode(self):
        self.vprint("BlokusGridFrame.enable_hover_mode: binding keys", 2)
        self.fixed_bind("<Motion>", self.mirror_showgrid)
        self.fixed_bind("<Button-1>", self.play)
        self.fixed_bind("<Right>", lambda event: self.rotate_cw())
        self.fixed_bind("<Left>", lambda event: self.rotate_ccw())
        self.fixed_bind("<Up>", lambda event: self.next_piece())
        self.fixed_bind("<Down>", lambda event: self.previous_piece())
        self.fixed_bind("<x>", lambda event: self.reflect_x())
        self.fixed_bind("<y>", lambda event: self.reflect_y())
        self.canvas.bind_all("<Enter>", self.mouse_over_handler)
        self.canvas.bind_all("<Leave>", self.mouse_off_handler)        
        self.enable_motion = True
        if len(self.current_pieces):
            self.mirror_showgrid()
    def vprint(self, msg, level):
        if level <= self.verbosity:
            print(self.verbose_levels[level] + ": "+msg)
    def disable_hover_mode(self):
        self.vprint("BlokusGridFrame.disable_hover_mode: releasing keys", 2)
        self.fixed_unbind("<Motion>")
        self.fixed_unbind("<Button-1>")
        self.fixed_unbind("<Right>")
        self.fixed_unbind("<Left>")
        self.fixed_unbind("<Up>")
        self.fixed_unbind("<x>")
        self.fixed_unbind('<y>')
        self.canvas.unbind('<Enter>')
        self.canvas.unbind('<Leave>')
        self.enable_motion = False
        if len(self.current_pieces):
            self.mirror_showgrid()
    def toggle_hover_mode(self):
        if self.enable_motion:
            self.disable_hover_mode()
        else:
            self.enable_hover_mode()
    def update_grid(self):
        for x in range(20):
            for y in range(20):
                self.canvas.itemconfig(y*20 + (x+1), fill=self.show_board[y][x][0], outline=self.show_board[y][x][1], width=self.show_board[y][x][2])
    def mirror_showgrid(self, event=None):
        if not self.mouse_over:
            return
        self.show_board = []
        board = self.board.board
        chg_x = self.width//20
        chg_y = self.height//20
        if event is None:
            x = self.mouse_coords[0]
            y = self.mouse_coords[1]
        else:
            x = event.x//chg_x
            y = event.y//chg_y
            self.mouse_coords = (x, y)
        piece = self.current_piece
        coords = piece.coords
        if not self.enable_motion:
            self.vprint('BlokusGridFrame.mirror_showgrid: motion not enabled', 2)
            coords = []
        coordinate_piece = [(x+coord[0], y+coord[1]) for coord in coords]
        for item in coordinate_piece:
            if item[0] > 19 or item[0] < 0 or item[1] > 19 or item[1] < 0:
                return self.board
        can_play = self.board.can_play_piece(piece, x, y, self.current_piece_firstmove)
        self.vprint("BlokusGridFrame.mirror_showgrid: Placement decision: "+str(can_play), 2)
        can_play = can_play[0]
        for x in range(20):
            cr = []
            for y in range(20):
                if (x,y) in coordinate_piece:
                    if can_play:
                        cr.append((self.piece_colors[board[y][x]], self.hover_outline_good, (self.height//20)/5))
                    else:
                        cr.append((self.piece_colors[board[y][x]], self.hover_outline_bad, (self.height//20)/5))
                else:
                    cr.append((self.piece_colors[board[y][x]], 'black', 1))
            self.show_board.append(cr)

            
        self.update_grid()
    def play(self, event):
        if self.board.can_play_piece(self.current_piece, self.mouse_coords[0], self.mouse_coords[1], self.current_piece_firstmove)[0]:
            self.board.play_piece(self.current_piece, self.mouse_coords[0], self.mouse_coords[1])
            self.last_move = (self.current_piece, self.mouse_coords[0], self.mouse_coords[1])
            self.vprint("BlokusGridFrame.play: played piece", 2)
            self.disable_hover_mode()
            self.mirror_showgrid()
            self.played_hook(self.current_selected_piece)

        else:
            self.vprint("BlokusGridFrame.play: could not play piece!", 1)




# TEST CODE


# import random
# w = tkinter.Tk(className='BlokusGridFrame - Test')
# w.title("BlokusGridFrame - Test")
# w.config(height=500, width=500)
# def wait_for_move_renew(event):
#     pass
# b = BlokusGridFrame(w, 250, 250, 280, 280, enable_motion=True)
# b.update_current_pieces(pieces.return_pieces(), 2, firstmove=True)
# blokus_board = b.board
# def play_random(event):
#     blokus_board.play_piece(BlokusPiece(pieces.return_pieces()[random.randint(0, 20)], random.randint(1, 4)), random.randint(0, 19), random.randint(0, 19))
#     b.mirror_showgrid()
# blokus_board.play_piece(BlokusPiece(pieces.return_pieces()[5], 2), 15, 15)
# w.after(5000, lambda: print(str(w.focus_get())))
# w.mainloop()