# piece values

WHITE = 0
BLACK = 1

WHITE_PAWN = 0
WHITE_KNIGHT = 1
WHITE_BISHOP = 2
WHITE_ROOK = 3
WHITE_QUEEN = 4
WHITE_KING = 5

BLACK_PAWN = 6
BLACK_KNIGHT = 7
BLACK_BISHOP = 8
BLACK_ROOK = 9
BLACK_QUEEN = 10
BLACK_KING = 11

EMPTY = -1

# castling rights:

# bit 0: white kingside
# bit 1: white queenside
# bit 2: black kingside
# bit 3: black queenside

WK = 1 << 0  # 0001
WQ = 1 << 1  # 0010
BK = 1 << 2  # 0100
BQ = 1 << 3  # 1000

# Move representation flags (bit 12-15)

QUIET = 0

DOUBLE_PAWN_PUSH = 1

KING_CASTLE = 2
QUEEN_CASTLE = 3

EN_PASSANT = 4

PROMOTE_N = 5
PROMOTE_B = 6
PROMOTE_R = 7
PROMOTE_Q = 8

# Pieces in printed board

pieces = {
    0: "P",
    1: "N",
    2: "B",
    3: "R",
    4: "Q",
    5: "K",
    6: "p",
    7: "n",
    8: "b",
    9: "r",
    10: "q",
    11: "k",
}

# Piece movement

KNIGHT_OFFSETS = [
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
]

KING_OFFSETS = [
    (1, 1),
    (1, -1),
    (1, 0),
    (-1, 1),
    (-1, -1),
    (-1, 0),
    (0, 1),
    (0, -1),
]

WHITE_PAWN_CAPTURE_OFFSETS = [
    (1, -1),
    (1, 1),
]

BLACK_PAWN_CAPTURE_OFFSETS = [
    (-1, -1),
    (-1, 1),
]

DIAGONAL_DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

ORTHOGONAL_DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Conversions used for uci conversion

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]

REVERSE_FILES = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
