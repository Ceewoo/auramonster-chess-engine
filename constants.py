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

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]

REVERSE_FILES = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
