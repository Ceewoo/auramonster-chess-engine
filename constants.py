white = 0
black = 1

white_pawn = 0
white_knight = 1
white_bishop = 2
white_rook = 3
white_queen = 4
white_king = 5

black_pawn = 6
black_knight = 7
black_bishop = 8
black_rook = 9
black_queen = 10
black_king = 11

empty = -1

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
    (-1, -1),
    (-1, 1),
]

BLACK_PAWN_CAPTURE_OFFSETS = [
    (1, -1),
    (1, 1),
]
