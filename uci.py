from constants import FILES, REVERSE_FILES
from movegen import generate_moves
from basefunctions import decode_move


def square_to_uci(square):

    rank = square // 8
    file = square % 8

    return FILES[file] + str(rank + 1)


def move_to_uci(encoded_move):
    from_sq, to_sq = decode_move(encoded_move)[0:2]

    return square_to_uci(from_sq) + square_to_uci(to_sq)


def parse_uci_move(board, uci_move):
    promoted_piece = None
    "g1f3"
    from_sq = REVERSE_FILES[uci_move[0]] + (int(uci_move[1]) - 1) * 8
    to_sq = REVERSE_FILES[uci_move[2]] + (int(uci_move[3]) - 1) * 8
    if len(uci_move) > 4:
        promoted_piece = uci_move[-1]
    for move in generate_moves(board):
        _from_sq, _to_sq, _flag = decode_move(move)
        if _from_sq == from_sq and _to_sq == to_sq:
            return move
