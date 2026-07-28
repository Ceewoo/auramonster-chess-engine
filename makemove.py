from basefunctions import decode_move
from constants import *


def make_move(encoded_move, board):

    from_sq, to_sq, flag = decode_move(encoded_move)

    piece = board.pieces[from_sq]
    side_to_move = board.side_to_move
    from_bb = 1 << from_sq
    to_bb = 1 << to_sq

    if side_to_move == WHITE:

        if flag == EN_PASSANT:
            captured = board.pieces[to_sq - 8]
            board.bitboards[captured] ^= to_bb << 8
        else:
            captured = board.pieces[to_sq]
            if captured != EMPTY:
                board.bitboards[captured] ^= to_bb

        if flag >= PROMOTE_N:
            promoted_piece = {
                PROMOTE_N: WHITE_KNIGHT,
                PROMOTE_B: WHITE_BISHOP,
                PROMOTE_R: WHITE_ROOK,
                PROMOTE_Q: WHITE_QUEEN,
            }[flag]

    undo = (
        piece,
        captured,
        board.white_occ,
        board.black_occ,
    )

    board.pieces[from_sq] = EMPTY
    board.pieces[to_sq] = piece

    if captured != EMPTY:
        if side_to_move == WHITE:
            if flag == EN_PASSANT:
                board.black_occ &= ~captured_sq
            else:
                board.black_occ &= ~to_bb
        else:
            board.white_occ &= ~to_bb
        board.bitboards[captured] ^= to_bb

    board.bitboards[piece] ^= from_bb
    board.bitboards[piece] ^= to_bb

    if side_to_move == WHITE:
        board.white_occ ^= from_bb
        board.white_occ ^= to_bb
        board.side_to_move = BLACK
    else:
        board.black_occ ^= from_bb
        board.black_occ ^= to_bb
        board.side_to_move = WHITE

    board.occupied = board.white_occ | board.black_occ

    return undo


def undo_move(encoded_move, undo, board):

    from_sq, to_sq, flag = decode_move(encoded_move)

    piece, captured, white_occ, black_occ = undo

    from_bb = 1 << from_sq
    to_bb = 1 << to_sq
    occupied = white_occ | black_occ

    if board.side_to_move == WHITE:
        side_to_move = BLACK
    else:
        side_to_move = WHITE

    board.pieces[from_sq] = piece
    if flag == EN_PASSANT:
        if side_to_move == WHITE:
            board.pieces[to_sq - 8] = captured
        else:
            board.pieces[to_sq + 8] = captured
    else:
        board.pieces[to_sq] = captured

    if captured != EMPTY:
        board.bitboards[captured] ^= to_bb

    board.bitboards[piece] ^= from_bb
    board.bitboards[piece] ^= to_bb

    board.side_to_move = side_to_move
    board.white_occ = white_occ
    board.black_occ = black_occ
    board.occupied = occupied
