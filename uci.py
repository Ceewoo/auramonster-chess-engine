from constants import FILES, REVERSE_FILES
from movegen import generate_moves
from basefunctions import decode_move

promoted_piece_number = {
    "n": 5,
    "b": 6,
    "r": 7,
    "q": 8,
}


def square_to_uci(square):

    rank = square // 8
    file = square % 8

    return FILES[file] + str(rank + 1)


def move_to_uci(encoded_move):
    from_sq, to_sq, flag = decode_move(encoded_move)

    if flag >= 5:
        if flag == 5:
            promotion = "n"
        elif flag == 6:
            promotion = "b"
        elif flag == 7:
            promotion = "r"
        else:
            promotion = "q"
        return square_to_uci(from_sq) + square_to_uci(to_sq) + promotion

    return square_to_uci(from_sq) + square_to_uci(to_sq)


def parse_uci_move(board, uci_move):
    promoted_piece = None
    from_sq = REVERSE_FILES[uci_move[0]] + (int(uci_move[1]) - 1) * 8
    to_sq = REVERSE_FILES[uci_move[2]] + (int(uci_move[3]) - 1) * 8
    if len(uci_move) > 4:
        promoted_piece = uci_move[-1]
    for move in generate_moves(board):
        _from_sq, _to_sq, _flag = decode_move(move)
        if _from_sq == from_sq and _to_sq == to_sq:
            if promoted_piece is None:
                return move
            if _flag == promoted_piece_number[promoted_piece]:
                return move
