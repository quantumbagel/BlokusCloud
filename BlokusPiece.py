class BlokusPiece:
    def __init__(self, coords: list[tuple], color: int) -> None:
        self.coords = coords
        self.color = color
    def rotate_cw(self):
        updated_coords = []
        for coord in self.coords:
            updated_coords.append((-coord[1], coord[0]))
        self.coords = updated_coords
    def rotate_ccw(self):
        updated_coords = []
        for coord in self.coords:
            updated_coords.append((coord[1], -coord[0]))
        self.coords = updated_coords
    def reflect_x(self):
        updated_coords = []
        for coord in self.coords:
            updated_coords.append((-coord[0], coord[1]))
        self.coords = updated_coords
    def reflect_y(self):
        updated_coords = []
        for coord in self.coords:
            updated_coords.append((coord[0], -coord[1]))
        self.coords = updated_coords
    def __str__(self) -> str:
        min_y = -min([coord[1] for coord in self.coords])
        min_x = -min([coord[0] for coord in self.coords])
        box_y = max([coord[1] for coord in self.coords])+min_y
        box_x = max([coord[0] for coord in self.coords])+min_x
        filled = '[]'
        not_filled = '  '
        out = ''
        new_coords = [(coord[0]+min_x, coord[1]+min_y) for coord in self.coords]
        last_x = 0
        for y in range(box_y+1):
            for x in range(box_x+1):
                if (x, y) in new_coords:
                    out += filled
                else:
                    out += not_filled
            out += '\n'
        return out[:-1]
