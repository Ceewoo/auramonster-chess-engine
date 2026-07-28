from basefunctions import decode_move
from constants import *


def make_move(encoded_move, board):

    from_sq, to_sq, flag = decode_move(encoded_move)

    piece = board.pieces[from_sq]
    side_to_move = board.side_to_move
    from_bb = 1 << from_sq
    to_bb = 1 << to_sq
    captured = EMPTY

    undo1 = (piece, board.white_occ, board.black_occ, board.en_passant, board.castling)

    if side_to_move == WHITE:

        if flag == DOUBLE_PAWN_PUSH:
            board.en_passant = to_sq - 8
        else:
            board.en_passant = -1

        if flag == EN_PASSANT:
            captured = board.pieces[to_sq - 8]
            board.bitboards[captured] ^= to_bb << 8
            board.black_occ ^= to_bb << 8
            board.pieces[to_sq - 8] = EMPTY

        elif flag == KING_CASTLE:
            board.bitboards[WHITE_ROOK] ^= 1 << 7
            board.bitboards[WHITE_ROOK] ^= 1 << 5
            board.white_occ ^= 1 << 7
            board.white_occ ^= 1 << 5
            board.pieces[7] = EMPTY
            board.pieces[5] = WHITE_ROOK
            board.castling &= ~WK
            board.castling &= ~WQ

        elif flag == QUEEN_CASTLE:
            board.bitboards[WHITE_ROOK] ^= 1 << 0
            board.bitboards[WHITE_ROOK] ^= 1 << 3
            board.white_occ ^= 1 << 0
            board.white_occ ^= 1 << 3
            board.pieces[0] = EMPTY
            board.pieces[3] = WHITE_ROOK
            board.castling &= ~WK
            board.castling &= ~WQ

        elif flag >= PROMOTE_N:
            promoted_piece = {
                PROMOTE_N: WHITE_KNIGHT,
                PROMOTE_B: WHITE_BISHOP,
                PROMOTE_R: WHITE_ROOK,
                PROMOTE_Q: WHITE_QUEEN,
            }[flag]

            captured = board.pieces[to_sq]
            if captured != EMPTY:
                board.bitboards[captured] ^= to_bb
                board.black_occ ^= to_bb

        else:
            captured = board.pieces[to_sq]
            if captured != EMPTY:
                board.bitboards[captured] ^= to_bb
                board.black_occ ^= to_bb
                if captured == BLACK_ROOK:
                    if to_sq == 0:
                        board.castling &= ~BQ
                    elif to_sq == 7:
                        board.castling &= ~BK

        if piece == WHITE_KING:
            board.castling &= ~WK
            board.castling &= ~WQ
        elif piece == WHITE_ROOK:
            if from_sq == 0:
                board.castling &= ~WQ
            elif from_sq == 7:
                board.castling &= ~WK

        board.white_occ ^= from_bb
        board.white_occ ^= to_bb
        board.side_to_move = BLACK

    else:

        if flag == DOUBLE_PAWN_PUSH:
            board.en_passant = to_sq + 8
        else:
            board.en_passant = -1

        if flag == EN_PASSANT:
            captured = board.pieces[to_sq + 8]
            board.bitboards[captured] ^= to_bb >> 8
            board.white_occ ^= to_bb >> 8
            board.pieces[to_sq + 8] = EMPTY

        elif flag == KING_CASTLE:
            board.bitboards[BLACK_ROOK] ^= 1 << 63
            board.bitboards[BLACK_ROOK] ^= 1 << 61
            board.black_occ ^= 1 << 63
            board.black_occ ^= 1 << 61
            board.pieces[63] = EMPTY
            board.pieces[61] = BLACK_ROOK
            board.castling &= ~BK
            board.castling &= ~BQ

        elif flag == QUEEN_CASTLE:
            board.bitboards[BLACK_ROOK] ^= 1 << 56
            board.bitboards[BLACK_ROOK] ^= 1 << 59
            board.black_occ ^= 1 << 56
            board.black_occ ^= 1 << 59
            board.pieces[56] = EMPTY
            board.pieces[59] = BLACK_ROOK
            board.castling &= ~BK
            board.castling &= ~BQ

        elif flag >= PROMOTE_N:
            promoted_piece = {
                PROMOTE_N: BLACK_KNIGHT,
                PROMOTE_B: BLACK_BISHOP,
                PROMOTE_R: BLACK_ROOK,
                PROMOTE_Q: BLACK_QUEEN,
            }[flag]

            captured = board.pieces[to_sq]
            if captured != EMPTY:
                board.bitboards[captured] ^= to_bb
                board.white_occ ^= to_bb
                if captured == WHITE_ROOK:
                    if to_sq == 0:
                        board.castling &= ~WQ
                    elif to_sq == 7:
                        board.castling &= ~WK

        else:
            captured = board.pieces[to_sq]
            if captured != EMPTY:
                board.bitboards[captured] ^= to_bb
                board.white_occ ^= to_bb

        if piece == BLACK_KING:
            board.castling &= ~BK
            board.castling &= ~BQ
        elif piece == BLACK_ROOK:
            if from_sq == 56:
                board.castling &= ~BQ
            elif from_sq == 63:
                board.castling &= ~BK

        board.black_occ ^= from_bb
        board.black_occ ^= to_bb
        board.side_to_move = WHITE

    board.pieces[from_sq] = EMPTY
    board.bitboards[piece] ^= from_bb

    if flag >= PROMOTE_N:
        board.pieces[to_sq] = promoted_piece
        board.bitboards[promoted_piece] ^= to_bb
    else:
        board.pieces[to_sq] = piece
        board.bitboards[piece] ^= to_bb

    board.occupied = board.white_occ | board.black_occ

    return undo1, captured


def undo_move(encoded_move, undo1, undo2, board):

    from_sq, to_sq, flag = decode_move(encoded_move)

    piece, white_occ, black_occ, old_en_passant, old_castling = undo1
    captured = undo2

    from_bb = 1 << from_sq
    to_bb = 1 << to_sq
    occupied = white_occ | black_occ

    if board.side_to_move == WHITE:
        side_to_move = BLACK
    else:
        side_to_move = WHITE

    board.pieces[from_sq] = piece

    if side_to_move == WHITE:
        if flag == EN_PASSANT:
            board.pieces[to_sq] = EMPTY
            board.pieces[to_sq - 8] = captured
        else:
            board.pieces[to_sq] = captured

        if captured != EMPTY:
            if flag == EN_PASSANT:
                board.bitboards[captured] ^= to_bb << 8
            else:
                board.bitboards[captured] ^= to_bb

        if flag == KING_CASTLE:
            board.pieces[7] = WHITE_ROOK
            board.pieces[5] = EMPTY
            board.bitboards[WHITE_ROOK] ^= 1 << 7
            board.bitboards[WHITE_ROOK] ^= 1 << 5

        elif flag == QUEEN_CASTLE:
            board.pieces[0] = WHITE_ROOK
            board.pieces[3] = EMPTY
            board.bitboards[WHITE_ROOK] ^= 1 << 0
            board.bitboards[WHITE_ROOK] ^= 1 << 3

        elif flag >= PROMOTE_N:
            promoted_piece = {
                PROMOTE_N: WHITE_KNIGHT,
                PROMOTE_B: WHITE_BISHOP,
                PROMOTE_R: WHITE_ROOK,
                PROMOTE_Q: WHITE_QUEEN,
            }[flag]

    else:
        if flag == EN_PASSANT:
            board.pieces[to_sq] = EMPTY
            board.pieces[to_sq + 8] = captured
        else:
            board.pieces[to_sq] = captured

        if captured != EMPTY:
            if flag == EN_PASSANT:
                board.pieces[to_sq] = EMPTY
                board.bitboards[captured] ^= to_bb >> 8
            else:
                board.bitboards[captured] ^= to_bb

        if flag == KING_CASTLE:
            board.pieces[63] = BLACK_ROOK
            board.pieces[61] = EMPTY
            board.bitboards[BLACK_ROOK] ^= 1 << 63
            board.bitboards[BLACK_ROOK] ^= 1 << 61

        elif flag == QUEEN_CASTLE:
            board.pieces[56] = BLACK_ROOK
            board.pieces[59] = EMPTY
            board.bitboards[BLACK_ROOK] ^= 1 << 56
            board.bitboards[BLACK_ROOK] ^= 1 << 59

        elif flag >= PROMOTE_N:
            promoted_piece = {
                PROMOTE_N: BLACK_KNIGHT,
                PROMOTE_B: BLACK_BISHOP,
                PROMOTE_R: BLACK_ROOK,
                PROMOTE_Q: BLACK_QUEEN,
            }[flag]

    board.bitboards[piece] ^= from_bb
    if flag >= PROMOTE_N:
        board.bitboards[promoted_piece] ^= to_bb
    else:
        board.bitboards[piece] ^= to_bb

    board.side_to_move = side_to_move
    board.white_occ = white_occ
    board.black_occ = black_occ
    board.occupied = occupied
    board.en_passant = old_en_passant
    board.castling = old_castling
