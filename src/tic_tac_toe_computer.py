import re
import time
import copy 
import random

BOARD_SIZE = 9
PLAYERS_ABBR = {'U': 'You', 'C': 'Computer'}
PLAYER_SWITCH = {'U': 'C', 'C': 'U'}

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
            winner = PLAYERS_ABBR[winner]
            print("WON! winner player: %s!" % winner)
            return winner
        func_won(*arg, **kw)

    return wrapper


class TicTacToeComputer(object):

    def __init__(self):
        self.player = 'U'
        self.total_moves = 0

        self.__set_available_moves()
        self.__generate_board()
        self.print_board()

    def __set_available_moves(self):
        self.available_moves = [
                        (0,0), (0,1), (0,2),
                        (1,0), (1,1), (1,2),
                        (2,0), (2,1), (2,2)
                    ]

    def __generate_board(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def print_board(self):
        bt = BOARD_TEMPLATE
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                place = "%s%s"%(row, column)
                value = " %s"%self.board[row][column]
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
            print("Example 1: 00")
            print("Example 2: 02")
            return False

        self.row, self.column = TicTacToeComputer.enrich_item(input_str)
        return True

    def computer_decision(self):
        def finding_winning_possibility(for_user):
            board = copy.deepcopy(self.board)
            c_row, c_col = None, None
            for (avail_row, avail_col) in self.available_moves:
                board[avail_row][avail_col] = for_user

                diagonal_1 = [board[i][j] for i in range(len(board)) for j in range(len(board)) if i == j]
                if all(diagonal_1) and len(set(diagonal_1)) == 1:
                    return avail_row, avail_col

                diagonal_2 = [board[i][j] for i in range(len(board)) for j in range(len(board)) if len(board) - 1 - i == j]
                if all(diagonal_2) and len(set(diagonal_2)) == 1:
                    return avail_row, avail_col

                for i in range(len(board)):
                    row = [board[i][j] for j in range(len(board))]
                    if all(row) and len(set(row)) == 1:
                        return avail_row, avail_col

                for i in range(len(board)):
                    column = [board[j][i] for j in range(len(board))]
                    if all(column) and len(set(column)) == 1:
                        return avail_row, avail_col

                board[avail_row][avail_col] = 0
            return None

        win_pos_computer = finding_winning_possibility(for_user='C')
        if win_pos_computer:
            return win_pos_computer

        win_pos_user = finding_winning_possibility(for_user='U')
        if win_pos_user:
            return win_pos_user

        return random.choice(self.available_moves)

    def update_move(self, player=None):
        if player == 'computer':
            print ("---- Computer is making decision ----")
            self.row, self.column = self.computer_decision()
            time.sleep(1)
            print ("Computer decided to go with move: %s%s" %(self.row, self.column))

        self.board[self.row][self.column] = self.player
        self.available_moves.remove((self.row, self.column))
        
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
        self.player = 'U'
        self.total_moves = 0

        self.__set_available_moves()
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
            print("- - - - - - - - - - - - - - - - - - -")
            input_str = input("\nEnter your move: ")
            if self.verify_n_set_input(input_str):
                if self.is_place_available():

                    self.update_move(player='user')
                    if self.won() or self.no_moves_left():
                        if self.end_game():
                            return
                        else:
                            continue
                    self.switch_player()

                    self.update_move(player='computer')            
                    if self.won() or self.no_moves_left():
                        if self.end_game():
                            return
                        else:
                            continue
                    self.switch_player()

                else:
                    print("The place you have selected was already reserved!")


if __name__ == '__main__':
    ttt = TicTacToeComputer()
    ttt.start_game()
