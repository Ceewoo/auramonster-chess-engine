from attacks import *
from constants import *
from basefunctions import pop_lsb


def add_check(board, king_square, checker_square, slider=False):
    if board.num_checkers == 0:
        board.check_mask = 0

    if slider:
        board.check_mask |= between[checker_square][king_square]

    board.check_mask |= 1 << checker_square
    board.num_checkers += 1


def check_status(board):

    board.pin_masks = [0] * 64
    board.check_mask = (1 << 64) - 1
    board.num_checkers = 0

    if board.side_to_move == WHITE:
        by_side = BLACK
        own_occ = board.white_occ
        king_square = pop_lsb(board.bitboards[WHITE_KING])[0]
        king_bb = 1 << king_square

        pawns = board.bitboards[BLACK_PAWN]
        knights = board.bitboards[BLACK_KNIGHT]
        bishops = board.bitboards[BLACK_BISHOP]
        rooks = board.bitboards[BLACK_ROOK]
        queens = board.bitboards[BLACK_QUEEN]

    else:
        by_side = WHITE
        own_occ = board.black_occ
        king_square = pop_lsb(board.bitboards[BLACK_KING])[0]
        king_bb = 1 << king_square

        pawns = board.bitboards[WHITE_PAWN]
        knights = board.bitboards[WHITE_KNIGHT]
        bishops = board.bitboards[WHITE_BISHOP]
        rooks = board.bitboards[WHITE_ROOK]
        queens = board.bitboards[WHITE_QUEEN]

    # Check scan

    while pawns:
        square, pawns = pop_lsb(pawns)

        if pawn_attacks(square, by_side) & king_bb:
            add_check(board, king_square, square)

    while knights:
        square, knights = pop_lsb(knights)

        if knight_attacks(square) & king_bb:
            add_check(board, king_square, square)

    while bishops:
        square, bishops = pop_lsb(bishops)

        if bishop_attacks(square, board.occupied) & king_bb:
            add_check(board, king_square, square, slider=True)

    while rooks:
        square, rooks = pop_lsb(rooks)

        if rook_attacks(square, board.occupied) & king_bb:
            add_check(board, king_square, square, slider=True)

    while queens:
        square, queens = pop_lsb(queens)

        if queen_attacks(square, board.occupied) & king_bb:
            add_check(board, king_square, square, slider=True)

    # Pin scan

    for step in TRUE_ORTHOGONAL_DIRS:
        sq = king_square + step
        blocker = None

        while 0 <= sq <= 63:
            bb = 1 << sq

            if board.occupied & bb:

                if own_occ & bb:

                    if blocker is None:
                        blocker = sq
                    else:
                        break

                else:

                    piece = board.pieces[sq]

                    if blocker is not None:
                        if board.side_to_move == WHITE:
                            if piece in (BLACK_ROOK, BLACK_QUEEN):
                                board.pin_masks[blocker] = between[king_square][sq] | bb
                        else:
                            if piece in (WHITE_ROOK, WHITE_QUEEN):
                                board.pin_masks[blocker] = between[king_square][sq] | bb

                    break

            sq += step

    for step in TRUE_DIAGONAL_DIRS:
        sq = king_square + step
        blocker = None

        while 0 <= sq <= 63:
            bb = 1 << sq

            if board.occupied & bb:

                if own_occ & bb:

                    if blocker is None:
                        blocker = sq
                    else:
                        break

                else:

                    piece = board.pieces[sq]

                    if blocker is not None:
                        if board.side_to_move == WHITE:
                            if piece in (BLACK_BISHOP, BLACK_QUEEN):
                                board.pin_masks[blocker] = between[king_square][sq] | bb
                        else:
                            if piece in (WHITE_BISHOP, WHITE_QUEEN):
                                board.pin_masks[blocker] = between[king_square][sq] | bb

                    break

            sq += step


def square_attacked(target_square, by_side, board):
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
