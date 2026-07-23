from constants import *


class Board:
    def __init__(self):
        self.bitboards = [0] * 12

        self.white_occ = 0
        self.black_occ = 0
        self.occupied = 0

        self.side_to_move = white

    def initialize_bitboard(self, fen=None):
        if not fen:
            self.bitboards[white_pawn] = 0x000000000000FF00
            self.bitboards[white_knight] = 0x0000000000000042
            self.bitboards[white_bishop] = 0x0000000000000024
            self.bitboards[white_rook] = 0x0000000000000081
            self.bitboards[white_queen] = 0x0000000000000010
            self.bitboards[white_king] = 0x0000000000000008

            self.bitboards[black_pawn] = 0x00FF000000000000
            self.bitboards[black_knight] = 0x4200000000000000
            self.bitboards[black_bishop] = 0x2400000000000000
            self.bitboards[black_rook] = 0x8100000000000000
            self.bitboards[black_queen] = 0x1000000000000000
            self.bitboards[black_king] = 0x0800000000000000
        else:
            pass

        for piece in range(6):
            self.white_occ |= self.bitboards[piece]
        for piece in range(6, 12):
            self.black_occ |= self.bitboards[piece]

        self.occupied = self.white_occ | self.black_occ
        print(self.occupied)

    def print_bitboard(self):
        for rank in range(7, -1, -1):
            for file in range(7, -1, -1):
                empty = 0
                sq = rank * 8 + file
                for piece in range(12):
                    if self.bitboards[piece] & 1 << sq:
                        print(pieces[piece], end=" ")
                        empty = 1
                        break
                if empty == 0:
                    print(".", end=" ")
            print("\n")

    def update_bitboard(self):
        return


board = Board()
board.initialize_bitboard()
board.print_bitboard()
