from . import main as game


def setup_function():
    game.fill_board()


def test_initial_board_and_case_normalization():
    assert len(game.board) == 32
    assert game.check_empty("A2", "player1") == -1
    assert game.piece_check("a8", "player2") == "rook"


def test_each_pawn_retains_its_own_first_move():
    assert game.is_legal_move("a2", "a4", "player1", capture_required=False)
    assert not game.board["a2"]["has_moved"]
    assert game.is_legal_move("b2", "b4", "player1", capture_required=False)


def test_pawn_cannot_jump_over_a_piece():
    game.board["a3"] = game.create_piece("knight", "player2")
    assert not game.is_legal_move("a2", "a4", "player1", capture_required=False)


def test_rook_checks_shape_and_entire_path():
    game.board.clear()
    game.board["d4"] = game.create_piece("rook", "player1")
    assert all(
        game.is_legal_move("d4", destination, "player1", capture_required=False)
        for destination in ("d1", "d8", "a4", "h4")
    )
    assert not game.is_legal_move("d4", "e5", "player1", capture_required=False)

    game.board["d6"] = game.create_piece("pawn", "player2")
    assert not game.is_legal_move("d4", "d8", "player1", capture_required=False)


def test_bishop_moves_in_all_four_directions_and_stops_at_blockers():
    game.board.clear()
    game.board["d4"] = game.create_piece("bishop", "player1")
    assert all(
        game.is_legal_move("d4", destination, "player1", capture_required=False)
        for destination in ("a1", "a7", "g1", "g7")
    )

    game.board["e5"] = game.create_piece("pawn", "player2")
    assert not game.is_legal_move("d4", "g7", "player1", capture_required=False)


def test_queen_combines_rook_and_bishop_movement_only():
    game.board.clear()
    game.board["d4"] = game.create_piece("queen", "player1")
    assert game.is_legal_move("d4", "d8", "player1", capture_required=False)
    assert game.is_legal_move("d4", "h8", "player1", capture_required=False)
    assert not game.is_legal_move("d4", "f5", "player1", capture_required=False)


def test_move_and_capture_are_distinguished():
    game.board.clear()
    game.board["a1"] = game.create_piece("rook", "player1")
    game.board["a4"] = game.create_piece("pawn", "player2")
    assert game.is_legal_move("a1", "a2", "player1", capture_required=False)
    assert not game.is_legal_move("a1", "a4", "player1", capture_required=False)
    assert game.is_legal_move("a1", "a4", "player1", capture_required=True)


def test_applying_capture_updates_board_piece_state_and_score():
    game.board.clear()
    game.scores["player1"] = 0
    game.board["a1"] = game.create_piece("rook", "player1")
    game.board["a4"] = game.create_piece("bishop", "player2")
    original_clear_square = game.pieces.clear_square
    original_draw_piece = game.draw_piece
    original_update = game.turtle.update
    try:
        game.pieces.clear_square = lambda location: None
        game.draw_piece = lambda location, piece: None
        game.turtle.update = lambda: None
        captured = game.move_piece("a4", "a1", "player1")
    finally:
        game.pieces.clear_square = original_clear_square
        game.draw_piece = original_draw_piece
        game.turtle.update = original_update

    assert captured["kind"] == "bishop"
    assert "a1" not in game.board
    assert game.board["a4"]["kind"] == "rook"
    assert game.board["a4"]["has_moved"]
    assert game.scores["player1"] == 3


TESTS = (
    test_initial_board_and_case_normalization,
    test_each_pawn_retains_its_own_first_move,
    test_pawn_cannot_jump_over_a_piece,
    test_rook_checks_shape_and_entire_path,
    test_bishop_moves_in_all_four_directions_and_stops_at_blockers,
    test_queen_combines_rook_and_bishop_movement_only,
    test_move_and_capture_are_distinguished,
    test_applying_capture_updates_board_piece_state_and_score,
)


def run_tests():
    for test in TESTS:
        setup_function()
        test()
    print(f"{len(TESTS)} rule tests passed")


if __name__ == "__main__":
    run_tests()
