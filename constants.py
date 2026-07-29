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

# Convert pieces from FEN

FEN_PIECES = {
    "P": WHITE_PAWN,
    "N": WHITE_KNIGHT,
    "B": WHITE_BISHOP,
    "R": WHITE_ROOK,
    "Q": WHITE_QUEEN,
    "K": WHITE_KING,
    "p": BLACK_PAWN,
    "n": BLACK_KNIGHT,
    "b": BLACK_BISHOP,
    "r": BLACK_ROOK,
    "q": BLACK_QUEEN,
    "k": BLACK_KING,
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

TRUE_DIAGONAL_DIRS = [9, 7, -7, -9]

TRUE_ORTHOGONAL_DIRS = [8, 1, -1, -8]

# Conversions used for uci conversion

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]

REVERSE_FILES = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


# Computes the squares between an attacker and its target

between = [[0] * 64 for _ in range(64)]

for attacker_square in range(64):
    rank_attacker, file_attacker = divmod(attacker_square, 8)

    for target_square in range(64):
        if attacker_square == target_square:
            continue

        rank_target, file_target = divmod(target_square, 8)

        dr = rank_target - rank_attacker
        df = file_target - file_attacker

        step = None

        if rank_attacker == rank_target:
            if df > 0:
                step = 1
            else:
                step = -1

        elif file_attacker == file_target:
            if dr > 0:
                step = 8
            else:
                step = -8

        elif abs(dr) == abs(df):
            if dr > 0 and df > 0:
                step = 9
            elif dr > 0 and df < 0:
                step = 7
            elif dr < 0 and df < 0:
                step = -9
            else:
                step = -7

        if step is None:
            continue

        sq = attacker_square + step
        mask = 0

        while sq != target_square:
            mask |= 1 << sq
            sq += step

        between[attacker_square][target_square] = mask
