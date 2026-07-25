from basefunctions import decode_move
from constants import *


def make_move(encoded_move, board):

    from_sq, to_sq, flag = decode_move(encoded_move)

    piece = board.pieces[from_sq]
    captured = board.pieces[to_sq]
    from_bb = 1 << from_sq
    to_bb = 1 << to_sq
    side_to_move = board.side_to_move

    undo = [
        from_sq,
        to_sq,
        flag,
        piece,
        captured,
        from_bb,
        to_bb,
        side_to_move,
        board.white_occ,
        board.black_occ,
        board.occupied,
    ]

    board.pieces[from_sq] = EMPTY
    board.pieces[to_sq] = piece

    if captured != EMPTY:
        if side_to_move == WHITE:
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


def undo_move(undo, board):

    from_sq = undo[0]
    to_sq = undo[1]
    flag = undo[2]
    piece = undo[3]
    captured = undo[4]
    from_bb = undo[5]
    to_bb = undo[6]
    side_to_move = undo[7]
    white_occ = undo[8]
    black_occ = undo[9]
    occupied = undo[10]

    board.pieces[from_sq] = piece
    board.pieces[to_sq] = captured

    if captured != EMPTY:
        board.bitboards[captured] ^= to_bb

    board.bitboards[piece] ^= from_bb
    board.bitboards[piece] ^= to_bb

    board.side_to_move = side_to_move
    board.white_occ = white_occ
    board.black_occ = black_occ
    board.occupied = occupied
