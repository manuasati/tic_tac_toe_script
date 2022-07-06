import re

PLAYERS = [1, 2]
PLAYER_SWITCH = {1:2, 2:1}

WINNING_NUMBER = 15
BORAD_SIZE = 9

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

class TicTacToeNumBased(object):
    def __init__(self):
        self.player = 1
        self.current_moves = 0
        self.__generate_board()
        self.__generate_allowed_moves()
        
        self.print_board()    

    def __generate_board(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def __generate_allowed_moves(self):
        self.players_allowed_moves = {
            1: [1, 3, 5, 7, 9], 
            2: [2, 4, 6, 8]
        }
        
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

    def who_won(self):
        #diagona1: [(0, 0), (1, 1), (2, 2)]
        diagonal_1 = [self.board[i][j] for i in range(len(self.board)) for j in range(len(self.board)) if i==j]
        if all(diagonal_1) and (sum(diagonal_1) == WINNING_NUMBER):
            return self.player

        #diagona1: [(0, 2), (1, 1), (2, 0)]
        diagonal_2 = [self.board[i][j] for i in range(len(self.board)) for j in range(len(self.board)) if (len(self.board)-1-i)==j]
        if all(diagonal_2) and (sum(diagonal_2) == WINNING_NUMBER):
            return self.player

        #rows
        for i in range(len(self.board)):
            row = [self.board[i][j] for j in range(len(self.board))]
            if all(row) and (sum(row) == WINNING_NUMBER):
                return self.player

        #columns
        for i in range(len(self.board)):
            column = [self.board[j][i] for j in range(len(self.board))]
            if all(column) and (sum(column) == WINNING_NUMBER):
                return self.player

        return None

    def no_moves_left(self):
        return all([self.board[i][j] for i in range(len(self.board)) for j in range(len(self.board))])

    @staticmethod
    def enrich_input_item(items):
        return [int(i) for i in items.replace(":", "")]

    def verify_n_set_input(self, input_str):
        input_str = input_str.replace(" ", "").strip()
        if not re.search("^[0-2]{1}[0-2]{1}:[1-9]{1}$", input_str):
            print("Invalid input! please follow: row col: num")
            print("Example: 00: 2")
            print("Example: 01: 5")
            return False

        self.row, self.column, self.number = TicTacToeNumBased.enrich_input_item(input_str)
        allowed_moves = self.players_allowed_moves[self.player]
        if self.number not in allowed_moves:
            print("Allowed moves for player '%s' : %s " %(self.player, allowed_moves))
            return False

        return True

    def update_board(self):
        self.current_moves += 1
        self.board[self.row][self.column] = self.number
        self.players_allowed_moves[self.player].remove(self.number)
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
        print("\nGame is started again....!")
        self.player = 1
        self.current_moves = 0
        self.__generate_board()
        self.__generate_allowed_moves()
        self.print_board()

    def start_game(self):
        while True:
            print("- - - - - - - - - - - - - - - ")
            input_str = input("\nEnter move for player '%s': " %self.player)
            if self.verify_n_set_input(input_str):
                if self.board[self.row][self.column] == 0:
                    self.update_board()
                else:
                    print("The place you have selected was already reserved!")
                    continue

                if self.who_won():
                    print ("WON! Player '%s' is the winner!" %self.player)
                    if self.end_game():
                        return

                if self.current_moves == BORAD_SIZE: #or self.no_moves_left():
                    print ("DRAW!")
                    if self.end_game():
                        return
                    else:
                        continue

                self.switch_player()


if __name__ == '__main__':
    ttt = TicTacToeNumBased()
    ttt.start_game()