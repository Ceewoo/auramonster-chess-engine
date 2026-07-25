from attacks import *
from constants import *
from basefunctions import pop_lsb, encode_move
from makemove import make_move, undo_move
from legal import is_square_attacked


def generate_moves(board):

    moves = []
    legal_moves = []

    side_to_move = board.side_to_move

    if side_to_move == WHITE:

        pawns = board.bitboards[WHITE_PAWN]
        knights = board.bitboards[WHITE_KNIGHT]
        bishops = board.bitboards[WHITE_BISHOP]
        rooks = board.bitboards[WHITE_ROOK]
        queens = board.bitboards[WHITE_QUEEN]

        king_square = board.bitboards[WHITE_KING].bit_length() - 1
        attacks = king_attacks(king_square)

        attacks &= ~board.white_occ

        while attacks:
            target, attacks = pop_lsb(attacks)
            moves.append(encode_move(king_square, target))

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, side_to_move)
            pushes = pawn_pushes(square, side_to_move)
            double_pushes = pawn_double_pushes(square, side_to_move)
            attacks &= board.black_occ
            pushes &= ~board.occupied
            double_pushes &= ~board.occupied
            double_pushes &= ~(board.occupied << 8)

            while attacks:
                target, attacks = pop_lsb(attacks)

                moves.append(encode_move(square, target))

            while pushes:
                target, pushes = pop_lsb(pushes)

                moves.append(encode_move(square, target))

            while double_pushes:
                target, double_pushes = pop_lsb(double_pushes)

                moves.append(encode_move(square, target))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)

            attacks &= ~board.white_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)

            attacks &= ~board.white_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)

            attacks &= ~board.white_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)

            attacks &= ~board.white_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        for move in moves:

            undo = make_move(move, board)

            king_square = board.bitboards[WHITE_KING].bit_length() - 1

            if not is_square_attacked(king_square, BLACK, board):
                legal_moves.append(move)

            undo_move(undo, board)

    else:

        pawns = board.bitboards[BLACK_PAWN]
        knights = board.bitboards[BLACK_KNIGHT]
        bishops = board.bitboards[BLACK_BISHOP]
        rooks = board.bitboards[BLACK_ROOK]
        queens = board.bitboards[BLACK_QUEEN]

        king_square = board.bitboards[BLACK_KING].bit_length() - 1
        attacks = king_attacks(king_square)

        attacks &= ~board.black_occ

        while attacks:
            target, attacks = pop_lsb(attacks)
            moves.append(encode_move(king_square, target))

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, side_to_move)
            pushes = pawn_pushes(square, side_to_move)
            double_pushes = pawn_double_pushes(square, side_to_move)
            attacks &= board.white_occ
            pushes &= ~board.occupied
            double_pushes &= ~board.occupied
            double_pushes &= ~(board.occupied >> 8)

            while attacks:
                target, attacks = pop_lsb(attacks)

                moves.append(encode_move(square, target))

            while pushes:
                target, pushes = pop_lsb(pushes)

                moves.append(encode_move(square, target))

            while double_pushes:
                target, double_pushes = pop_lsb(double_pushes)

                moves.append(encode_move(square, target))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)

            attacks &= ~board.black_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)

            attacks &= ~board.black_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)

            attacks &= ~board.black_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)

            attacks &= ~board.black_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        for move in moves:

            undo = make_move(move, board)

            king_square = board.bitboards[BLACK_KING].bit_length() - 1

            if not is_square_attacked(king_square, WHITE, board):
                legal_moves.append(move)

            undo_move(undo, board)

    return legal_moves
