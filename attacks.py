from constants import (
    KNIGHT_OFFSETS,
    KING_OFFSETS,
    WHITE_PAWN_CAPTURE_OFFSETS,
    BLACK_PAWN_CAPTURE_OFFSETS,
    WHITE,
    BLACK,
    DIAGONAL_DIRS,
    ORTHOGONAL_DIRS,
)

from basefunctions import inside_board, get_bit

_KNIGHT_ATTACKS = [0] * 64
_KING_ATTACKS = [0] * 64
_PAWN_ATTACKS = [[0] * 64 for _ in range(2)]
_PAWN_PUSH = [[0] * 64 for _ in range(2)]
_PAWN_DOUBLE_PUSH = [[0] * 64 for _ in range(2)]


def init_tables():
    init_knight_attacks()
    init_king_attacks()
    init_pawn_attacks()
    init_pawn_pushes()
    init_pawn_double_pushes()


def init_knight_attacks():
    for square in range(64):
        rank = square // 8
        file = square % 8

        attacks = 0

        for dr, df in KNIGHT_OFFSETS:
            new_rank = rank + dr
            new_file = file + df

            if inside_board(new_rank, new_file):
                target = new_rank * 8 + new_file

                attacks |= 1 << target

        _KNIGHT_ATTACKS[square] = attacks


def init_king_attacks():
    for square in range(64):
        rank = square // 8
        file = square % 8

        attacks = 0

        for dr, df in KING_OFFSETS:
            new_rank = rank + dr
            new_file = file + df

            if inside_board(new_rank, new_file):
                target = new_rank * 8 + new_file

                attacks |= 1 << target

        _KING_ATTACKS[square] = attacks


def init_pawn_attacks():
    for square in range(64):
        rank = square // 8
        file = square % 8

        attacks = 0

        for dr, df in WHITE_PAWN_CAPTURE_OFFSETS:
            new_rank = rank + dr
            new_file = file + df

            if inside_board(new_rank, new_file):

                target = new_rank * 8 + new_file

                attacks |= 1 << target

        _PAWN_ATTACKS[WHITE][square] = attacks

    for square in range(64):
        rank = square // 8
        file = square % 8

        attacks = 0

        for dr, df in BLACK_PAWN_CAPTURE_OFFSETS:
            new_rank = rank + dr
            new_file = file + df

            if inside_board(new_rank, new_file):

                target = new_rank * 8 + new_file

                attacks |= 1 << target

        _PAWN_ATTACKS[BLACK][square] = attacks


def init_pawn_pushes():

    for square in range(64):
        new_rank = square // 8 + 1
        new_file = square % 8

        attacks = 0

        if inside_board(new_rank, new_file):
            target = new_rank * 8 + new_file

            attacks |= 1 << target

        _PAWN_PUSH[WHITE][square] = attacks

    for square in range(64):
        new_rank = square // 8 - 1
        new_file = square % 8

        attacks = 0

        if inside_board(new_rank, new_file):
            target = new_rank * 8 + new_file

            attacks |= 1 << target

        _PAWN_PUSH[BLACK][square] = attacks


def init_pawn_double_pushes():

    for square in range(64):
        new_rank = square // 8 + 2
        new_file = square % 8

        attacks = 0

        if new_rank == 3 and 0 <= new_file <= 7:
            target = 24 + new_file

            attacks |= 1 << target

        _PAWN_DOUBLE_PUSH[WHITE][square] = attacks

    for square in range(64):
        new_rank = square // 8 - 2
        new_file = square % 8

        attacks = 0

        if new_rank == 4 and 0 <= new_file <= 7:
            target = 32 + new_file

            attacks |= 1 << target

        _PAWN_DOUBLE_PUSH[BLACK][square] = attacks


def knight_attacks(square):
    return _KNIGHT_ATTACKS[square]


def king_attacks(square):
    return _KING_ATTACKS[square]


def pawn_attacks(square, color):
    return _PAWN_ATTACKS[color][square]


def bishop_attacks(square, occupied):
    rank = square // 8
    file = square % 8

    attacks = 0

    for dr, df in DIAGONAL_DIRS:

        new_rank = rank + dr
        new_file = file + df

        while inside_board(new_rank, new_file):

            target = new_rank * 8 + new_file

            attacks |= 1 << target

            if get_bit(occupied, target):
                break

            new_rank += dr
            new_file += df

    return attacks


def rook_attacks(square, occupied):

    rank = square // 8
    file = square % 8

    attacks = 0

    for dr, df in ORTHOGONAL_DIRS:

        new_rank = rank + dr
        new_file = file + df

        while inside_board(new_rank, new_file):

            target = new_rank * 8 + new_file

            attacks |= 1 << target

            if get_bit(occupied, target):
                break

            new_rank += dr
            new_file += df

    return attacks


def queen_attacks(square, occupied):
    return bishop_attacks(square, occupied) | rook_attacks(square, occupied)


def pawn_pushes(square, color):  # not an attack
    return _PAWN_PUSH[color][square]


def pawn_double_pushes(square, color):  # not an attack
    return _PAWN_DOUBLE_PUSH[color][square]
