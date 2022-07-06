import pytest

from src.tic_tac_toe import TicTacToe

def test_switch_player():
    ttt = TicTacToe()
    assert ttt.player == 'X'

    ttt.switch_player()
    assert ttt.player == 'O'

    ttt.switch_player()
    assert ttt.player == 'X'


@pytest.mark.parametrize(
    "total_moves, response", 
    [(9, True), (2, False), (5, False), (8, False)]
)
def test_no_moves_left(total_moves, response):
    ttt = TicTacToe()

    ttt.total_moves = total_moves
    assert ttt.no_moves_left() == response


@pytest.mark.parametrize(
    "board_row_colum_list, input_row_column, response", 
    [
        ( [(0, 0), (1, 0)], (2, 0), True),
        ( [(1, 0), (2, 0), (2, 1)], (1, 1), True),
        ( [(1, 0), (1, 2), (2, 0)], (1, 0), False),
        ( [(1, 0), (2, 0), (2, 1), (2, 2)], (2, 2), False),
    ]
)
def test_is_place_available(board_row_colum_list, input_row_column, response):
    ttt = TicTacToe()

    for (r, c) in board_row_colum_list:
        ttt.board[r][c] = ttt.player

    ttt.row, ttt.column = input_row_column
    assert ttt.is_place_available() == response

        
@pytest.mark.parametrize(
    "input_str, response", 
    [
        ( "00", True),
        ( "01", True),
        ( "20", True),
        ( "22", True),

        ( "", False),
        ( "0", False),
        ( "200", False),
        ( "00X", False),
        ( "00O", False),
        ( "AA00", False),
        ( "0,0", False),
        ( "0,0:X", False),
    ]
)
def test_verify_n_set_input(input_str, response):
    ttt = TicTacToe()

    assert ttt.verify_n_set_input(input_str) == response
    if response == True:
        assert [ttt.row, ttt.column] == [int(i) for i in input_str]


def test_restart_game():
    ttt = TicTacToe()

    ttt.player = 'O'
    ttt.total_moves = 9
    ttt.board = [ ['X', 1, 0], [2, "x", 0], [3, 0, 0] ]

    ttt.restart_game()

    assert ttt.player == 'X'
    assert ttt.total_moves == 0
    assert ttt.board == [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]


@pytest.mark.parametrize(
    "board, response", 
    [
        ( [ ['O', 'X', 'X'], [0, 0, 0], [0, 0, 0] ], None),
        ( [ ['X', 'X', 'X'], [0, 0, 0], [0, 0, 0] ], True),
        ( [ ['O', 0, 'X'], [0, 'X', 0], ['X', 0, 0] ], True),
        ( [ ['O', 'X', 'X'], [0, 0, 0], [0, 0, 0] ], None),
        ( [ [0, 0, 0], ['O', 'O', 'O'], [0, 0, 0] ], True),
    ]
)
def test_won(board, response):
    ttt = TicTacToe()

    ttt.board = board
    if response:
        assert ttt.won() == ttt.player
    else:
        assert ttt.won() == response