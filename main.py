import turtle
import chessboard
import pieces

HEADERS = "abcdefgh"
BOARD_SIZE = 480
PLAYER_COLORS = {"player1": "white", "player2": "black"}
PIECE_VALUES = {
    "pawn": 1,
    "knight": 3,
    "bishop": 3,
    "rook": 5,
    "queen": 9,
    "king": 0,
}

CYAN = "\033[96m"
YELLOW = "\033[93m"
DEFAULT = "\033[0m"

board = {}
scores = {"player1": 0, "player2": 0}
valid_moves = {file_name + str(rank) for file_name in HEADERS for rank in range(1, 9)}


def normalize_location(location):
    return location.strip().lower()

def create_piece(kind, player):
    return {
        "kind": kind,
        "player": player,
        "color": PLAYER_COLORS[player],
        "value": PIECE_VALUES[kind],
        "has_moved": False,
    }

def fill_board():
    board.clear()
    scores.update({"player1": 0, "player2": 0})
    back_rank = ("rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook")

    for player, pawn_rank, piece_rank in (
        ("player1", 2, 1),
        ("player2", 7, 8),
    ):
        for file_name in HEADERS:
            board[file_name + str(pawn_rank)] = create_piece("pawn", player)
        for file_name, kind in zip(HEADERS, back_rank):
            board[file_name + str(piece_rank)] = create_piece(kind, player)

def check_empty(location, player): # Return 0 for empty, -1 for friendly, or 1 for enemy.
    piece = board.get(normalize_location(location))
    if piece is None:
        return 0
    return -1 if piece["player"] == player else 1

def piece_check(location, player):
    piece = board.get(normalize_location(location))
    if piece is not None and piece["player"] == player:
        return piece["kind"]
    return ""

def square_coordinates(location):
    location = normalize_location(location)
    return HEADERS.index(location[0]), int(location[1])

def squares_between(curr_loc, dest_loc): # test squares in between
    curr_col, curr_row = square_coordinates(curr_loc)
    dest_col, dest_row = square_coordinates(dest_loc)
    col_diff = dest_col - curr_col
    row_diff = dest_row - curr_row

    if col_diff != 0 and row_diff != 0 and abs(col_diff) != abs(row_diff):
        return None

    col_step = (col_diff > 0) - (col_diff < 0)
    row_step = (row_diff > 0) - (row_diff < 0)
    if col_step == 0 and row_step == 0:
        return None

    squares = []
    col = curr_col + col_step
    row = curr_row + row_step
    while (col, row) != (dest_col, dest_row):
        squares.append(HEADERS[col] + str(row))
        col += col_step
        row += row_step
    return squares

def path_is_clear(curr_loc, dest_loc):
    path = squares_between(curr_loc, dest_loc)
    return path is not None and all(square not in board for square in path)

def check_move_pawn(dest_loc, curr_loc, player, is_capture=False):
    piece = board.get(normalize_location(curr_loc))
    if piece is None or piece["kind"] != "pawn" or piece["player"] != player:
        return False

    curr_col, curr_row = square_coordinates(curr_loc)
    dest_col, dest_row = square_coordinates(dest_loc)
    direction = 1 if player == "player1" else -1
    col_diff = dest_col - curr_col
    row_diff = dest_row - curr_row

    if is_capture:
        return abs(col_diff) == 1 and row_diff == direction
    if col_diff != 0:
        return False
    if row_diff == direction:
        return True

    starting_rank = 2 if player == "player1" else 7
    if not piece["has_moved"] and curr_row == starting_rank and row_diff == 2 * direction:
        middle_square = HEADERS[curr_col] + str(curr_row + direction)
        return middle_square not in board
    return False

def check_rook(dest_loc, curr_loc, player=None):
    curr_col, curr_row = square_coordinates(curr_loc)
    dest_col, dest_row = square_coordinates(dest_loc)
    if curr_col != dest_col and curr_row != dest_row:
        return False
    return path_is_clear(curr_loc, dest_loc)

def check_knight(dest_loc, curr_loc):
    curr_col, curr_row = square_coordinates(curr_loc)
    dest_col, dest_row = square_coordinates(dest_loc)
    return sorted((abs(dest_col - curr_col), abs(dest_row - curr_row))) == [1, 2]

def check_move_bishop(dest_loc, curr_loc, player=None):
    curr_col, curr_row = square_coordinates(curr_loc)
    dest_col, dest_row = square_coordinates(dest_loc)
    if abs(dest_col - curr_col) != abs(dest_row - curr_row):
        return False
    return path_is_clear(curr_loc, dest_loc)

def check_queen(dest_loc, curr_loc, player=None):
    return check_move_bishop(dest_loc, curr_loc) or check_rook(dest_loc, curr_loc)

def check_king(dest_loc, curr_loc):
    curr_col, curr_row = square_coordinates(curr_loc)
    dest_col, dest_row = square_coordinates(dest_loc)
    col_diff = abs(dest_col - curr_col)
    row_diff = abs(dest_row - curr_row)
    return max(col_diff, row_diff) == 1

def movement_is_valid(piece, curr_loc, dest_loc, is_capture):
    kind = piece["kind"]
    if kind == "pawn":
        return check_move_pawn(dest_loc, curr_loc, piece["player"], is_capture)
    if kind == "rook":
        return check_rook(dest_loc, curr_loc)
    if kind == "knight":
        return check_knight(dest_loc, curr_loc)
    if kind == "bishop":
        return check_move_bishop(dest_loc, curr_loc)
    if kind == "queen":
        return check_queen(dest_loc, curr_loc)
    if kind == "king":
        return check_king(dest_loc, curr_loc)
    return False

def is_legal_move(curr_loc, dest_loc, player, capture_required=None):
    curr_loc = normalize_location(curr_loc)
    dest_loc = normalize_location(dest_loc)
    if curr_loc not in valid_moves or dest_loc not in valid_moves or curr_loc == dest_loc:
        return False

    piece = board.get(curr_loc)
    if piece is None or piece["player"] != player:
        return False

    destination_piece = board.get(dest_loc)
    if destination_piece is not None and destination_piece["player"] == player:
        return False

    is_capture = destination_piece is not None
    if capture_required is True and not is_capture:
        return False
    if capture_required is False and is_capture:
        return False
    return movement_is_valid(piece, curr_loc, dest_loc, is_capture)

def draw_piece(location, piece):
    drawers = {
        "pawn": pieces.draw_pawn,
        "rook": pieces.draw_rook,
        "knight": pieces.draw_knight,
        "bishop": pieces.draw_bishop,
    }
    if piece["kind"] in drawers:
        drawers[piece["kind"]](piece["color"], location)
    else:
        pieces.draw_royalty(piece["color"], location, piece["kind"] == "queen")

def render_pieces():
    for location, piece in board.items():
        draw_piece(location, piece)

def move_piece(dest_loc, curr_loc, player): # move or capture
    curr_loc = normalize_location(curr_loc)
    dest_loc = normalize_location(dest_loc)
    moving_piece = board.pop(curr_loc)
    captured_piece = board.pop(dest_loc, None)

    pieces.clear_square(curr_loc)
    board[dest_loc] = moving_piece
    moving_piece["has_moved"] = True
    draw_piece(dest_loc, moving_piece)
    turtle.update()

    if captured_piece is not None:
        scores[player] += captured_piece["value"]
    return captured_piece

def valid_move(curr_loc, dest_loc, player):
    if not is_legal_move(curr_loc, dest_loc, player, capture_required=False):
        return False
    move_piece(dest_loc, curr_loc, player)
    return True

def valid_capture(curr_loc, dest_loc, player):
    if not is_legal_move(curr_loc, dest_loc, player, capture_required=True):
        return False
    move_piece(dest_loc, curr_loc, player)
    return True

def check_input(user_input, valid):
    user_input = user_input.strip().lower()
    while user_input not in valid:
        print("Hmm... I don't recognize that input.")
        user_input = input("Try again: ").strip().lower()
    return user_input

def prompt_for_piece(player):
    while True:
        current = check_input(
            input("Which piece do you want to use? Type its position or 'x' to go back: "),
            valid_moves | {"x"},
        )
        if current == "x":
            return None
        if piece_check(current, player):
            return current
        print("That isn't your piece.")

def take_turn(player, capture_required):
    current = prompt_for_piece(player)
    if current is None:
        return False, None

    while True:
        destination = check_input(
            input("Where do you want to go? Type the destination or 'x' to go back: "),
            valid_moves | {"x"},
        )
        if destination == "x":
            return False, None
        if is_legal_move(current, destination, player, capture_required):
            return True, move_piece(destination, current, player)
        print("That move isn't valid.")

def main():
    pieces.set_board_size(BOARD_SIZE)
    turtle.tracer(0, 0)
    chessboard.board(BOARD_SIZE)
    fill_board()
    render_pieces()
    turtle.update()

    print("Welcome to the chess game!")
    current_player = "player1"
    playing = True

    while playing:
        label_color = CYAN if current_player == "player1" else YELLOW
        print(f"{label_color}{current_player.title()}{DEFAULT} turn. Score: {scores[current_player]}")
        choice = check_input(
            input("Do you want to:\n1. Move\n2. Capture\n3. End Game\n: "),
            {"1", "2", "3", "move", "capture", "end", "m", "c", "e"},
        )
        if choice in {"3", "end", "e"}:
            break

        capture_required = choice in {"2", "capture", "c"}
        turn_completed, captured_piece = take_turn(current_player, capture_required)
        if not turn_completed:
            continue

        if captured_piece is not None:
            print(f"Captured {captured_piece['kind']}. Score: {scores[current_player]}")
            if captured_piece["kind"] == "king":
                print(f"{current_player.title()} wins!")
                playing = False
                continue

        current_player = "player2" if current_player == "player1" else "player1"

    turtle.done()


if __name__ == "__main__":
    main()
