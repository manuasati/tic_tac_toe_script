import re

BOARD_SIZE = 9
PLAYERS = ['X', 'O']
PLAYER_SWITCH = {'X': 'O', 'O': 'X'}

BOARD_TEMPLATE = '''
      0   1   2
    -------------
  0 |00 |01 |02 |
    -------------
  1 |10 |11 |12 |
    -------------
  2 |20 |21 |22 |
    -------------
'''

def print_winner_statement(func_won):

    def wrapper(*arg, **kw):
        winner = func_won(*arg, **kw)
        if winner:
            print("WON! Player '%s' is the winner!" % winner)
            return winner
        func_won(*arg, **kw)

    return wrapper


class TicTacToe(object):

    def __init__(self):
        self.player = 'X'
        self.total_moves = 0
        self.__generate_board()
        self.print_board()

    def __generate_board(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def print_board(self):
        bt = BOARD_TEMPLATE
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                place = "%s%s"%(i,j)
                value = " %s"%self.board[i][j]
                bt = bt.replace(place, value.replace("0", " "))
        print (bt)

    def switch_player(self):
        self.player = PLAYER_SWITCH[self.player]

    def no_moves_left(self):
        if self.total_moves == BOARD_SIZE:
            print("\n --  -- DRAW -- --\n")
        return self.total_moves == BOARD_SIZE

    def is_place_available(self):
        return self.board[self.row][self.column] == 0

    @staticmethod
    def enrich_item(items):
        return [int(i) for i in items]

    def verify_n_set_input(self, input_str):
        input_str = input_str.replace(" ", "").strip()
        if not re.search("^[0-2]{1}[0-2]{1}$", input_str):
            print("Invalid input! only 0, 1 or 2 are allowed.")
            print("(combination of 2 digit from 0, 1, 2)")
            print("Example 1: 00")
            print("Example 2: 02")
            return False

        self.row, self.column = TicTacToe.enrich_item(input_str)
        return True

    def update_board(self):
        self.board[self.row][self.column] = self.player
        self.total_moves += 1
        self.print_board()

    def end_game(self):
        next_step = input("Play again (yes/no)? ")
        if next_step.lower() == 'yes':
            self.restart_game()
            return False
        else:
            print("Exit!, Good bye!")
            return True

    def restart_game(self):
        print("Restarting game again....!")
        self.player = 'X'
        self.total_moves = 0
        self.__generate_board()
        self.print_board()

    @print_winner_statement
    def won(self):
        #diagonal: [(0,0), (1,1), (2,2)]
        diagonal_1 = [self.board[i][j] for i in range(
            len(self.board)) for j in range(len(self.board)) if i == j]
        if all(diagonal_1) and len(set(diagonal_1)) == 1:
            return self.player

        #diagonal: [(0,2), (1,1), (2,0)]
        diagonal_2 = [self.board[i][j] for i in range(len(self.board))
                      for j in range(len(self.board))
                      if len(self.board) - 1 - i == j]
        if all(diagonal_2) and len(set(diagonal_2)) == 1:
            return self.player

        #rows
        for i in range(len(self.board)):
            row = [self.board[i][j] for j in range(len(self.board))]
            if all(row) and len(set(row)) == 1:
                return self.player

        #column
        for i in range(len(self.board)):
            column = [self.board[j][i] for j in range(len(self.board))]
            if all(column) and len(set(column)) == 1:
                return self.player

        return None

    def start_game(self):
        while True:
            print("- - - - - - - - - - - - - - - ")
            input_str = input("\nEnter move for player '%s': " % self.player)
            if self.verify_n_set_input(input_str):
                if self.is_place_available():
                    self.update_board()
                else:
                    print("The place you have selected was already reserved!")
                    continue

                if self.won() or self.no_moves_left():
                    if self.end_game():
                        return
                    else:
                        continue

                self.switch_player()

if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.start_game()
