def won(self):
    def check_diagonal_1():
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if i==j and self.board[i][j]==0:
                    return False
        return True

    def check_diagonal_2():
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                left_idx = len(self.board)-1-i
                if left_idx==j and self.board[left_idx][j]==0:
                    return False
        return True

    def chec_in_row():
        for i in range(len(self.board)):
            player_count = 0
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    break
                player_count += 1
                if player_count == len(self.board):
                    return True
        return False

def no_more_moves():
    return all([self.board[i][j] for i in range(len(self.board)) for j in range(len(self.board))])
