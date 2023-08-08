from BlokusPiece import BlokusPiece
class BlokusBoard:
    def __init__(self, board=None) -> None:
        if board is None:
            self.board = [[0 for i in range(20)] for j in range(20)]
        else:
            self.board = board
    
    def can_play_piece(self, piece: BlokusPiece, x: int, y: int, first_move: bool):
        coordinates = piece.coords
        ok = False
        color = piece.color
        for coord in coordinates:
            y_c = coord[1]+y
            x_c = coord[0]+x
            if x_c > 19 or x_c < 0 or y_c > 19 or y_c < 0:
                return False, 'invalid space (couldn\'t place)'
            space = self.board[coord[1]+y][coord[0]+x]
            adj_neighbors = self._get_adj_neighbors(coord[0]+x, coord[1]+y)
            if not len(adj_neighbors): # invalid space
                return False, 'invalid space'
            for neighbor in adj_neighbors:
                if neighbor == color:
                    return False, 'adjacent neighbor is my color'
            diag_neighbors = self._get_diag_neighbors(coord[0]+x, coord[1]+y)
            for neighbor in diag_neighbors:
                if neighbor == color:
                    ok = True
                    break 
            if space:
                return False, 'playing on top of piece'
        if not ok:
            ch_const = 19
            if not first_move:
                return False, 'no neighboring diagonal neighbor'
            elif not (((-x, -y) in coordinates) or ((ch_const-x, -y) in coordinates) or ((ch_const-x, ch_const-y) in coordinates) or ((-x, ch_const-y) in coordinates)):
                return False, 'first move not on corner'
           
        return True, 'legal'
        
    def play_piece(self, piece: BlokusPiece, x: int, y: int):
        coordinates = piece.coords
        color = piece.color
        for coord in coordinates:
            self.board[coord[1]+y][coord[0]+x] = color
        print(self)
        
    def find_valid_playing_squares(self, color: int, first_move=False):
        squares = []
        for y in range(20):
            for x in range(20):
                location = self.board[y][x]
                neighbors_adj = self._get_adj_neighbors(x, y)
                neighbors_diag = self._get_diag_neighbors(x, y)
                check_adj = [i for i in neighbors_adj if i > 0 and i != color]
                check_diag = [i for i in neighbors_diag if i == color]
                if len(check_diag) and not len(check_adj) and location == 0:
                    squares.append((x, y))
        if first_move:
            for corner_piece in [(0,0), (0,19),(19,0),(19,19)]:
                if self.board[corner_piece[1]][corner_piece[0]] == 0:
                    squares.append(corner_piece)
        return squares
    def can_play(self, pieces: list[list[tuple]], color: int, first_move=False):
        valid_spaces = self.find_valid_playing_squares(color, first_move)
        legal_moves = []
        for rt in range(8):
            #print("Rt", rt)
            for p_num, piece in enumerate(pieces):
                #print("PNUM", p_num)
                bp = BlokusPiece(piece, color)
                for rotate in range(rt % 4):
                    bp.rotate_cw()
                if rt // 4:
                    bp.reflect_x()
                for v_num, valid_space in enumerate(valid_spaces):
                    #print("VNUM",v_num )
                    for s_num, square in enumerate(piece):
                        #print("SNUM", s_num)
                        rel_x = -square[0]
                        rel_y = -square[1]
                        new_piece = [(p[0]+rel_x, p[1]+rel_y) for p in piece]
                        new_bp = BlokusPiece(new_piece, color)
                        if self.can_play_piece(new_bp, valid_space[0], valid_space[1], first_move)[0]:
                            legal_moves.append((new_bp, valid_space[0], valid_space[1]))
        return legal_moves                    
    def _get_space_neighbors(self, x, y):
        if x < 0 or x > 19 or y < 0 or y > 19:
            return []
        spaces = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == dy == 0:
                    continue
                if x+dx < 0 or x+dx > 19:
                    continue
                if y+dy < 0 or y+dy > 19:
                    continue
                spaces.append(self.board[y+dy][x+dx])
        return spaces
    def _get_diag_neighbors(self, x: int, y: int):
        if x < 0 or x > 19 or y < 0 or y > 19:
            return []
        spaces = []
        for item in [(-1,1), (1,-1), (-1,-1), (1,1)]:
            dx = item[0]
            dy = item[1]
            if dx == dy == 0:
                continue
            if x+dx < 0 or x+dx > 19:
                continue
            if y+dy < 0 or y+dy > 19:
                continue
            spaces.append(self.board[y+dy][x+dx])
        return spaces
    def _get_adj_neighbors(self, x: int, y: int):
        if x < 0 or x > 19 or y < 0 or y > 19:
            return []
        spaces = []
        for item in [(0,1), (0,-1), (-1,0), (1,0)]:
            dx = item[0]
            dy = item[1]
            if dx == dy == 0:
                continue
            if x+dx < 0 or x+dx > 19:
                continue
            if y+dy < 0 or y+dy > 19:
                continue
            spaces.append(self.board[y+dy][x+dx])
        return spaces
    def __str__(self) -> str:
        out = ''
        for y in range(20):
            for x in range(20):
                if self.board[y][x]:
                    out += '['+str(self.board[y][x])+']'
                else:
                    out += '.'*3
            out += '\n'
        return out



