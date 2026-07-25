from attacks import *
from constants import *
from basefunctions import pop_lsb


def is_square_attacked(target_square, by_side, board):
    # by_side means that is the color attacking
    target_bb = 1 << target_square
    occupied = board.occupied

    if by_side == WHITE:
        pawns = board.bitboards[WHITE_PAWN]
        knights = board.bitboards[WHITE_KNIGHT]
        bishops = board.bitboards[WHITE_BISHOP]
        rooks = board.bitboards[WHITE_ROOK]
        queens = board.bitboards[WHITE_QUEEN]
        king = board.bitboards[WHITE_KING]

    else:
        pawns = board.bitboards[BLACK_PAWN]
        knights = board.bitboards[BLACK_KNIGHT]
        bishops = board.bitboards[BLACK_BISHOP]
        rooks = board.bitboards[BLACK_ROOK]
        queens = board.bitboards[BLACK_QUEEN]
        king = board.bitboards[BLACK_KING]

    square = pop_lsb(king)[0]
    if king_attacks(square) & target_bb:
        return 1

    while pawns:
        square, pawns = pop_lsb(pawns)

        if pawn_attacks(square, by_side) & target_bb:
            return 1

    while knights:
        square, knights = pop_lsb(knights)

        if knight_attacks(square) & target_bb:
            return 1

    while bishops:
        square, bishops = pop_lsb(bishops)

        if bishop_attacks(square, occupied) & target_bb:
            return 1

    while rooks:
        square, rooks = pop_lsb(rooks)

        if rook_attacks(square, occupied) & target_bb:
            return 1

    while queens:
        square, queens = pop_lsb(queens)

        if queen_attacks(square, occupied) & target_bb:
            return 1

    return 0
