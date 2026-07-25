from board import Board
from makemove import make_move
from movegen import generate_moves
from attacks import init_tables
from uci import parse_uci_move

init_tables()
board = Board()


while True:
    board.print_bitboard()
    moves = generate_moves(board)
    move = input("Move:")
    encoded_move = parse_uci_move(board, move)
    if encoded_move in moves:
        make_move(encoded_move, board)
