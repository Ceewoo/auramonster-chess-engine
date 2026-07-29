from attacks import *
from constants import *
from basefunctions import pop_lsb, encode_move
from makemove import make_move, undo_move
from legal import *


def generate_moves(board):

    check_status(board)

    moves = []

    if board.num_checkers == 2:  # only king moves available
        if board.side_to_move == WHITE:
            king_square = board.bitboards[WHITE_KING].bit_length() - 1
            king_bb = 1 << king_square
            attacks = king_attacks(king_square)

            attacks &= ~board.white_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                board.bitboards[WHITE_KING] ^= king_bb
                board.white_occ ^= king_bb
                board.occupied ^= king_bb
                if not square_attacked(target, BLACK, board):
                    moves.append(encode_move(king_square, target))
                board.bitboards[WHITE_KING] ^= king_bb
                board.white_occ ^= king_bb
                board.occupied ^= king_bb

            return moves

        else:
            king_square = board.bitboards[BLACK_KING].bit_length() - 1
            king_bb = 1 << king_square
            attacks = king_attacks(king_square)

            attacks &= ~board.black_occ

            while attacks:
                target, attacks = pop_lsb(attacks)
                board.bitboards[BLACK_KING] ^= king_bb
                board.black_occ ^= king_bb
                board.occupied ^= king_bb
                if not square_attacked(target, WHITE, board):
                    moves.append(encode_move(king_square, target))
                board.bitboards[BLACK_KING] ^= king_bb
                board.black_occ ^= king_bb
                board.occupied ^= king_bb

            return moves

    side_to_move = board.side_to_move
    check_mask = board.check_mask
    pin_masks = board.pin_masks

    if side_to_move == WHITE:

        pawns = board.bitboards[WHITE_PAWN]
        knights = board.bitboards[WHITE_KNIGHT]
        bishops = board.bitboards[WHITE_BISHOP]
        rooks = board.bitboards[WHITE_ROOK]
        queens = board.bitboards[WHITE_QUEEN]

        king_square = board.bitboards[WHITE_KING].bit_length() - 1
        king_bb = 1 << king_square
        attacks = king_attacks(king_square)

        attacks &= ~board.white_occ

        if board.castling & WK:
            if not (board.occupied & ((1 << 5) | (1 << 6))):
                if (
                    not square_attacked(4, BLACK, board)
                    and not square_attacked(5, BLACK, board)
                    and not square_attacked(6, BLACK, board)
                ):
                    moves.append(encode_move(4, 6, KING_CASTLE))

        if board.castling & WQ:
            if not (board.occupied & ((1 << 3) | (1 << 2) | (1 << 1))):
                if (
                    not square_attacked(4, BLACK, board)
                    and not square_attacked(3, BLACK, board)
                    and not square_attacked(2, BLACK, board)
                ):
                    moves.append(encode_move(4, 2, QUEEN_CASTLE))

        while attacks:
            target, attacks = pop_lsb(attacks)

            board.bitboards[WHITE_KING] ^= king_bb
            board.white_occ ^= king_bb
            board.occupied ^= king_bb
            if not square_attacked(target, BLACK, board):
                moves.append(encode_move(king_square, target))
            board.bitboards[WHITE_KING] ^= king_bb
            board.white_occ ^= king_bb
            board.occupied ^= king_bb

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, side_to_move)
            pushes = pawn_pushes(square, side_to_move)
            double_pushes = pawn_double_pushes(square, side_to_move)
            capture_targets = board.black_occ
            if board.en_passant != -1:
                capture_targets |= 1 << board.en_passant

            attacks &= capture_targets
            pushes &= ~board.occupied
            double_pushes &= ~board.occupied
            double_pushes &= ~(board.occupied << 8)

            attacks &= check_mask
            pushes &= check_mask
            double_pushes &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask
                pushes &= pin_mask
                double_pushes &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                if target >= 56:
                    moves.append(encode_move(square, target, PROMOTE_N))
                    moves.append(encode_move(square, target, PROMOTE_B))
                    moves.append(encode_move(square, target, PROMOTE_R))
                    moves.append(encode_move(square, target, PROMOTE_Q))

                elif board.en_passant == target:
                    moves.append(encode_move(square, target, EN_PASSANT))

                else:
                    moves.append(encode_move(square, target))

            while pushes:
                target, pushes = pop_lsb(pushes)

                if target >= 56:
                    moves.append(encode_move(square, target, PROMOTE_N))
                    moves.append(encode_move(square, target, PROMOTE_B))
                    moves.append(encode_move(square, target, PROMOTE_R))
                    moves.append(encode_move(square, target, PROMOTE_Q))
                else:
                    moves.append(encode_move(square, target))

            while double_pushes:
                target, double_pushes = pop_lsb(double_pushes)

                moves.append(encode_move(square, target, DOUBLE_PAWN_PUSH))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)

            attacks &= ~board.white_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks = 0

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)

            attacks &= ~board.white_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)

            attacks &= ~board.white_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)

            attacks &= ~board.white_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

    else:

        pawns = board.bitboards[BLACK_PAWN]
        knights = board.bitboards[BLACK_KNIGHT]
        bishops = board.bitboards[BLACK_BISHOP]
        rooks = board.bitboards[BLACK_ROOK]
        queens = board.bitboards[BLACK_QUEEN]

        king_square = board.bitboards[BLACK_KING].bit_length() - 1
        king_bb = 1 << king_square
        attacks = king_attacks(king_square)

        attacks &= ~board.black_occ

        if board.castling & BK:
            if not (board.occupied & ((1 << 62) | (1 << 61))):
                if (
                    not square_attacked(60, WHITE, board)
                    and not square_attacked(61, WHITE, board)
                    and not square_attacked(62, WHITE, board)
                ):
                    moves.append(encode_move(60, 62, KING_CASTLE))

        if board.castling & BQ:
            if not (board.occupied & ((1 << 59) | (1 << 58) | (1 << 57))):
                if (
                    not square_attacked(60, WHITE, board)
                    and not square_attacked(59, WHITE, board)
                    and not square_attacked(58, WHITE, board)
                ):
                    moves.append(encode_move(60, 58, QUEEN_CASTLE))

        while attacks:
            target, attacks = pop_lsb(attacks)

            board.bitboards[BLACK_KING] ^= king_bb
            board.black_occ ^= king_bb
            board.occupied ^= king_bb
            if not square_attacked(target, WHITE, board):
                moves.append(encode_move(king_square, target))
            board.bitboards[BLACK_KING] ^= king_bb
            board.black_occ ^= king_bb
            board.occupied ^= king_bb

        while pawns:
            square, pawns = pop_lsb(pawns)
            attacks = pawn_attacks(square, side_to_move)
            pushes = pawn_pushes(square, side_to_move)
            double_pushes = pawn_double_pushes(square, side_to_move)
            capture_targets = board.white_occ
            if board.en_passant != -1:
                capture_targets |= 1 << board.en_passant

            attacks &= capture_targets
            pushes &= ~board.occupied
            double_pushes &= ~board.occupied
            double_pushes &= ~(board.occupied >> 8)

            attacks &= check_mask
            pushes &= check_mask
            double_pushes &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask
                pushes &= pin_mask
                double_pushes &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                if target <= 7:
                    moves.append(encode_move(square, target, PROMOTE_N))
                    moves.append(encode_move(square, target, PROMOTE_B))
                    moves.append(encode_move(square, target, PROMOTE_R))
                    moves.append(encode_move(square, target, PROMOTE_Q))

                elif board.en_passant == target:
                    moves.append(encode_move(square, target, EN_PASSANT))

                else:
                    moves.append(encode_move(square, target))

            while pushes:
                target, pushes = pop_lsb(pushes)

                if target <= 7:
                    moves.append(encode_move(square, target, PROMOTE_N))
                    moves.append(encode_move(square, target, PROMOTE_B))
                    moves.append(encode_move(square, target, PROMOTE_R))
                    moves.append(encode_move(square, target, PROMOTE_Q))
                else:
                    moves.append(encode_move(square, target))

            while double_pushes:
                target, double_pushes = pop_lsb(double_pushes)

                moves.append(encode_move(square, target, DOUBLE_PAWN_PUSH))

        while knights:
            square, knights = pop_lsb(knights)
            attacks = knight_attacks(square)

            attacks &= ~board.black_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks = 0

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while bishops:
            square, bishops = pop_lsb(bishops)
            attacks = bishop_attacks(square, board.occupied)

            attacks &= ~board.black_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while rooks:
            square, rooks = pop_lsb(rooks)
            attacks = rook_attacks(square, board.occupied)

            attacks &= ~board.black_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

        while queens:
            square, queens = pop_lsb(queens)
            attacks = queen_attacks(square, board.occupied)

            attacks &= ~board.black_occ
            attacks &= check_mask

            pin_mask = pin_masks[square]
            if pin_mask:
                attacks &= pin_mask

            while attacks:
                target, attacks = pop_lsb(attacks)
                moves.append(encode_move(square, target))

    return moves
