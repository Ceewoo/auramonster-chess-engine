from attacks import *
from constants import *
from basefunctions import pop_lsb, get_bit
from moves import encode_move


def generate_moves(board):

    moves = []

    if board.side_to_move == white:

        pawns = board.bitboards[white_pawn]
        knights = board.bitboards[white_knight]
        bishops = board.bitboards[white_bishop]
        rooks = board.bitboards[white_rook]
        queens = board.bitboards[white_queen]

        square = board.bitboards[white_king].bit_length() - 1
        attacks = king_attacks(square)
        for attack in attacks:
            if not get_bit(board.white_occ, attack):
                moves.append(encode_move(square, attack))

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, board.side_to_move)
            pushes = pawn_pushes(square, board.side_to_move)
            double_pushes = pawn_double_pushes(
                square, board.occupied, board.side_to_move
            )
            while attacks:
                attack, attacks = pop_lsb(attacks)
                if get_bit(board.black_occ, attack):
                    moves.append(encode_move(square, attack))

            while pushes:
                push, pushes = pop_lsb(attacks)
                if not get_bit(board.occupied, push):
                    moves.append(encode_move(square, push))

            while double_pushes:
                double_push, double_pushes = pop_lsb(attacks)
                if not get_bit(board.occupied, double_push) and not get_bit(
                    board.occupied, double_push - 8
                ):
                    moves.append(encode_move(square, double_push))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.white_occ):
                    moves.append(encode_move(square, attacks))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.white_occ):
                    moves.append(encode_move(square, attacks))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.white_occ):
                    moves.append(encode_move(square, attacks))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.white_occ):
                    moves.append(encode_move(square, attacks))

        return moves

    else:

        pawns = board.bitboards[black_pawn]
        knights = board.bitboards[black_knight]
        bishops = board.bitboards[black_bishop]
        rooks = board.bitboards[black_rook]
        queens = board.bitboards[black_queen]

        attacks = king_attacks(board.bitboards[black_king].bit_length() - 1)
        moves.append(encode_move(attacks))

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, board.side_to_move)
            pushes = pawn_pushes(square, board.side_to_move)
            double_pushes = pawn_double_pushes(
                square, board.occupied, board.side_to_move
            )

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if get_bit(board.white_occ, attack):
                    moves.append(encode_move(attack))

            while pushes:
                push, pushes = pop_lsb(attacks)
                if not get_bit(board.occupied, push):
                    moves.append(encode_move(push))

            while double_pushes:
                double_push, double_pushes = pop_lsb(attacks)
                if not get_bit(board.occupied, double_push) and not get_bit(
                    board.occupied, double_push + 8
                ):
                    moves.append(encode_move(double_push))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.black_occ):
                    moves.append(encode_move(attacks))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.black_occ):
                    moves.append(encode_move(attacks))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.black_occ):
                    moves.append(encode_move(attacks))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)

            while attacks:
                attack, attacks = pop_lsb(attacks)
                if not get_bit(board.black_occ):
                    moves.append(encode_move(attacks))

        return moves
