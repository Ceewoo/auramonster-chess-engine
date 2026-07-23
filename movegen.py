from attacks import *
from constants import *
from basefunctions import pop_lsb
from moves import encode_move


def generate_moves(board):

    moves = []

    if board.side_to_move == white:

        pawns = board.bitboards[white_pawn]
        knights = board.bitboards[white_knight]
        bishops = board.bitboards[white_bishop]
        rooks = board.bitboards[white_rook]
        queens = board.bitboards[white_queen]

        attacks = king_attacks(board.bitboards[white_king].bit_length() - 1)
        moves.append(encode_move(attacks))

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, board.side_to_move)
            moves.append(encode_move(attacks))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)
            moves.append(encode_move(attacks))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)
            moves.append(encode_move(attacks))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)
            moves.append(encode_move(attacks))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)
            moves.append(encode_move(attacks))

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
            moves.append(encode_move(attacks))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)
            moves.append(encode_move(attacks))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)
            moves.append(encode_move(attacks))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)
            moves.append(encode_move(attacks))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)
            moves.append(encode_move(attacks))

        return moves
