from constants import (
    KNIGHT_OFFSETS,
    KING_OFFSETS,
    WHITE_PAWN_CAPTURE_OFFSETS,
    BLACK_PAWN_CAPTURE_OFFSETS,
    white,
    black,
)

_KNIGHT_ATTACKS = [0] * 64
_KING_ATTACKS = [0] * 64
_PAWN_PUSH = [[0] * 64 for _ in range(2)]
_PAWN_DOUBLE_PUSH = [[0] * 64 for _ in range(2)]
_PAWN_ATTACKS = [[0] * 64 for _ in range(2)]


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

            if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
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

            if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
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

            if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
                if dr == -2:
                    if rank != 1:
                        continue
                target = new_rank * 8 + new_file

                attacks |= 1 << target

        _PAWN_ATTACKS[white][square] = attacks

    for square in range(64):
        rank = square // 8
        file = square % 8

        attacks = 0

        for dr, df in BLACK_PAWN_CAPTURE_OFFSETS:
            new_rank = rank + dr
            new_file = file + df

            if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
                if dr == 2:
                    if rank != 6:
                        continue
                target = new_rank * 8 + new_file

                attacks |= 1 << target

        _PAWN_ATTACKS[black][square] = attacks


def init_pawn_pushes():

    for square in range(64):
        new_rank = square // 8 + 1
        new_file = square % 8

        attacks = 0

        if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
            target = new_rank * 8 + new_file

            attacks |= 1 << target

        _PAWN_PUSH[white][square] = attacks

    for square in range(64):
        new_rank = square // 8 - 1
        new_file = square % 8

        attacks = 0

        if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
            target = new_rank * 8 + new_file

            attacks |= 1 << target

        _PAWN_PUSH[black][square] = attacks


def init_pawn_double_pushes():

    for square in range(64):
        new_rank = square // 8 + 2
        new_file = square % 8

        attacks = 0

        if new_rank == 3 and 0 <= new_file <= 7:
            target = 24 + new_file

            attacks |= 1 << target

        _PAWN_DOUBLE_PUSH[white][square] = attacks

    for square in range(64):
        new_rank = square // 8 - 2
        new_file = square % 8

        attacks = 0

        if new_rank == 4 and 0 <= new_file <= 7:
            target = 32 + new_file

            attacks |= 1 << target

        _PAWN_DOUBLE_PUSH[black][square] = attacks


def knight_attacks(square):
    return _KNIGHT_ATTACKS[square]


def king_attacks(square):
    return _KING_ATTACKS[square]


def pawn_attacks(square, color):
    return _PAWN_ATTACKS[square][color]


def bishop_attacks(square, occupied):
    return


def rook_attacks(square, occupied):
    return


def queen_attacks(square, occupied):
    return


# 36 = knight square
#
