from constants import *
from basefunctions import pop_lsb


class Board:
    def __init__(self):
        self.bitboards = [0] * 12

        self.pieces = [EMPTY] * 64

        self.white_occ = 0
        self.black_occ = 0
        self.occupied = 0

        self.side_to_move = WHITE
        self.castling = 1111
        self.en_passant = -1

        self.initialize_board()

    def initialize_board(self, fen=None):
        if not fen:
            self.bitboards[WHITE_PAWN] = 0x000000000000FF00
            self.bitboards[WHITE_KNIGHT] = 0x0000000000000042
            self.bitboards[WHITE_BISHOP] = 0x0000000000000024
            self.bitboards[WHITE_ROOK] = 0x0000000000000081
            self.bitboards[WHITE_QUEEN] = 0x0000000000000008
            self.bitboards[WHITE_KING] = 0x0000000000000010

            self.bitboards[BLACK_PAWN] = 0x00FF000000000000
            self.bitboards[BLACK_KNIGHT] = 0x4200000000000000
            self.bitboards[BLACK_BISHOP] = 0x2400000000000000
            self.bitboards[BLACK_ROOK] = 0x8100000000000000
            self.bitboards[BLACK_QUEEN] = 0x0800000000000000
            self.bitboards[BLACK_KING] = 0x1000000000000000
        else:
            pass

        for piece in range(12):
            bb = self.bitboards[piece]

            while bb:
                square, bb = pop_lsb(bb)
                self.pieces[square] = piece

        for piece in range(6):
            self.white_occ |= self.bitboards[piece]
        for piece in range(6, 12):
            self.black_occ |= self.bitboards[piece]

        self.occupied = self.white_occ | self.black_occ

    def print_bitboard(self):
        for rank in range(7, -1, -1):
            for file in range(8):
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
