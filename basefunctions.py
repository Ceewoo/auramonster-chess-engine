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


def pop_lsb(bb):
    square = (bb & -bb).bit_length() - 1
    bb &= bb - 1
    return square, bb  # remaining pieces


def inside_board(rank, file):
    return 0 <= rank <= 7 and 0 <= file <= 7


def get_bit(occupied, square):  # returns truthy if there is a piece on that square
    return occupied & 1 << square


def encode_move(
    from_sq,
    to_sq,
    flag=0,
):
    move = from_sq
    move |= to_sq << 6
    move |= flag << 12

    return move


def decode_move(move):
    from_sq = move & 0x3F
    to_sq = move >> 6 & 0x3F
    flag = move >> 12

    return from_sq, to_sq, flag
