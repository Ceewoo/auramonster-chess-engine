def perft(board, depth):
    if depth == 0:
        return 1

    nodes = 0

    encode_moves = board.generate_moves()

    for move in encode_moves:
        undo = board.make_move(move)[0]
        nodes += perft(board, depth - 1)
        board.undo_move(undo)

    return nodes


def divide(board, depth):
    total_nodes = 0

    encode_moves = board.generate_moves()

    for move in encode_moves:
        undo = board.make_move(move)[0]

        nodes = perft(board, depth - 1)

        board.undo_move(undo)

        # print(f"{move_to_uci(move)}: {nodes}")

        total_nodes += nodes

    print("-" * 30)
    print(f"Total: {total_nodes}")

    return total_nodes


def speedtest(total_time, moves):
    if moves == 25:
        print("-----------------")
        print(
            f"Average time spent per move in first 25 moves: {total_time / moves:.4f} seconds"
        )
    else:
        print("-----------------")
        print(f"Average time spent per move: {total_time / moves:.4f} seconds")


def effective_branching_factor(nodes, depth):
    low, high = 1.0, 50.0

    for _ in range(40):
        mid = (low + high) / 2

        total = 0
        for i in range(depth + 1):
            total += mid**i

        if total < nodes:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def pop_lsb(piece):
    lsb = piece & -piece
    square = lsb.bit_length() - 1
    piece &= piece - 1
    return square, piece  # remaining pieces
