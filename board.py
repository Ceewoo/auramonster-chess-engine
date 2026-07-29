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

        self.pin_masks = [0] * 64
        self.check_mask = 0
        self.num_checkers = 0

        self.castling = 0
        self.en_passant = -1

        self.halfmove_clock = 0

        self.FEN = "n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1"

        # FEN of starting position:
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        # FEN of Kiwipete:
        # r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1

        # FEN of promotion test:
        # n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1

        self.initialize_board()

    def initialize_board(self):
        self.load_fen(self.FEN)

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

    def load_fen(self, fen):
        board, side, castling, en_passant, halfmove, fullmove = fen.split()
        rows = board.split("/")
        for row, fen_row in enumerate(rows):
            col = 0
            for char in fen_row:
                if char in "PNBRQKpnbrqk":
                    square = (7 - row) * 8 + col
                    self.bitboards[FEN_PIECES[char]] |= 1 << square
                    col += 1
                else:
                    col += int(char)

        if side == "w":
            self.side_to_move = WHITE
        else:
            self.side_to_move = BLACK

        if "K" in castling:
            self.castling |= WK
        if "Q" in castling:
            self.castling |= WQ
        if "k" in castling:
            self.castling |= BK
        if "q" in castling:
            self.castling |= BQ

        if en_passant != "-":
            ep_square = REVERSE_FILES[en_passant[0]] + int(en_passant[1]) * 8
            self.en_passant = ep_square

        self.halfmove_clock = halfmove
