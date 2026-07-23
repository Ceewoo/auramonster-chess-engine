from board import Board
from moves import make_move
from makemove import generate_moves
from attacks import init_tables

init_tables()
board = Board()


while True:
    board.print_bitboard(board)
    moves = generate_moves(board)
    move = input("Move:")
    make_move(move, board)
