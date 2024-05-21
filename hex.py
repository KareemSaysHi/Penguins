class Hex:

    def __init__(self, q, r, s, hextype):
        assert (q + r + s) == 0, "q + r + s must be 0"
        self.q = q
        self.r = r
        self.s = s
        self.hextype = hextype #either penguin, white, blue, or support

    def get_coordinates(self):
        return self.q, self.r, self.s