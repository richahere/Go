class Game(object):
    def __init__(self):
        self.__size = 15
        self.__board = [[0 for i in range(self.__size)] for j in range(self.__size)]
        self.__ghost_board = self.__board.copy()
        self.__player_turn = 2
        self.one_6 = [  [0,1,1,1,1,1],[1,1,1,1,1,0],[0,1,1,1,1,0],[0,1,0,1,1,1],[1,1,1,0,1,0],[0,1,1,0,1,1],[1,1,0,1,1,0], [0,1,1,1,0,1],[1,0,1,1,1,0],[0,1,1,1,0,0],[0,0,1,1,1,0],[0,1,0,1,1,0],[0,1,1,0,1,0],[2,1,1,1,0,0],[0,0,1,1,1,2],[2,1,1,0,1,0],[0,1,0,1,1,2],[0,1,1,0,1,2],[2,1,0,1,1,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,1,1,2],[2,1,1,0,0,0],[0,0,1,0,1,2],[2,1,0,1,0,0],[0,1,0,0,1,2],[2,1,0,0,1,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[2,1,1,1,1,2]]
        self.score_6 = [100000000,10000000,10000000,500000,500000,500000,500000,500000,500000,100000,100000,100000,100000,500,500,500,500,500,500,50,50,5,5,5,5,5,5,1,1,0]
        self.one_5 = [  [1,1,1,1,1],[1,1,1,1,0],[0,1,1,1,1],[0,1,1,1,0],[1,0,0,1,1],[1,1,0,0,1],[1,0,1,0,1],[0,1,0,1,0], [1,0,0,0,1],[2,1,1,1,2],[2,1,1,2,0],[0,2,1,1,2],]
        self.score_5 = [10000000,10000,10000,100000,500,500,500,5,5,0,0,0]
        self.two_6 = [  [0,2,2,2,2,2],[2,2,2,2,2,0],[0,2,2,2,2,0],[0,2,0,2,2,2],[2,2,2,0,2,0],[0,2,2,0,2,2],[2,2,0,2,2,0],[0,2,2,2,0,2],[2,0,2,2,2,0],[0,1,1,1,0,0],[0,0,1,1,1,0],[0,2,0,2,2,0],[0,2,2,0,2,0], [1,2,2,2,0,0],[0,0,2,2,2,1],[1,2,2,0,2,0],[0,2,0,2,2,1],[0,2,2,0,2,1],[1,2,0,2,2,0],[0,0,2,2,0,0],[0,2,0,0,2,0],[0,0,0,2,2,1],[1,2,2,0,0,0],[0,0,2,0,2,1],[1,2,0,2,0,0],[0,2,0,0,2,1],[1,2,0,0,2,0],[0,0,2,0,0,0],[0,0,0,2,0,0],[1,2,2,2,2,1]]
        self.two_5 = [  [2,2,2,2,2],[2,2,2,2,0],[0,2,2,2,2],[0,2,2,2,0],[2,0,0,2,2],[2,2,0,0,2],[2,0,2,0,2],[0,2,0,2,0], [2,0,0,0,2],[1,2,2,2,1],[1,2,2,1,0],[0,1,2,2,1]]
    def get(self, row, col):
        if row < 0 or row >= self.__size or col < 0 or col >= self.__size:
            return 0
        return self.__board[row][col]
    def has_neighbor(self, row, col):
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
        if self.__board[row][col] != 0:
            return False
        for (xdirection, ydirection) in directions:
            if xdirection != 0 and ((col + xdirection) < 0 or (col + xdirection) >= self.__size):
                continue
            if ydirection != 0 and ((row + ydirection) < 0 or (row + ydirection) >= self.__size):
                continue
            if self.__board[row + ydirection][col + xdirection] != 0:
                return True
        return False
    def size(self):
        return self.__size
    def turn(self):
        return self.__player_turn
    def board(self):
        return self.__board  
    def sliding_window(self,iterable, size=5):
        i = iter(iterable)
        window = []
        for j in range(0, size):
            window.append(next(i))
        yield window
        for j in i:
            window = window[1:] + [j]
            yield window
    def evaluate(self, vec):
        score = {'one': 0, 'two': 0}
        count_one = 0
        count_two = 0
        if len(vec) == 5:
            for i in range(len(self.one_5)):
                if self.one_5[i] == vec:
                    score['one'] += self.score_5[i] * 1
                if self.two_5[i] == vec:
                    score['two'] += self.score_5[i] * 1
            return score
        generator = list(self.sliding_window(vec,5))
        for i in generator:
            for j in range(len(self.one_5)):
                if i==self.one_5[j]:
                    score['one'] += self.score_5[j] * len(generator) + len(generator)
                if i==self.two_5[j]:
                    score['two'] += self.score_5[j] * len(generator) + len(generator)
        generator = list(self.sliding_window(vec, 6))
        for i in generator:
            for j in range(len(self.one_6)):
                if i==self.one_6[j]:
                    score['one'] += self.score_6[j] * len(generator) + len(generator)
                if i==self.two_6[j]:
                    score['two'] += self.score_6[j] * len(generator) + len(generator)
        return score
    def evaluate_board_score(self):
        vectors = []
        board_score = 0
        for i in range(self.__size):
            vectors.append(self.__ghost_board[i])
        for j in range(0,self.__size):
            vectors.append(list(self.__ghost_board[x][j] for x in range(self.__size)))
        vectors.append(list(self.__ghost_board[x][x] for x in range(self.__size)))
        vectors.append(list(self.__ghost_board[x][self.__size - x - 1] for x in range(self.__size)))
        if self.__size >= 6:
            for i in range(1, self.__size - 4):
                vectors.append(list(self.__ghost_board[row][row - i] for row in range (i, self.__size)))
                vectors.append(list(self.__ghost_board[col - i][col] for col in range(i, self.__size)))
            for i in range(4, self.__size - 1):
                vectors.append(list(self.__ghost_board[i - x][x] for x in range(i, -1, -1)))
                vectors.append(list(self.__ghost_board[self.__size - 1 - x][self.__size - 1 - (i - x)] for x in range(i, -1, -1)))
        for v in vectors:
            mygenerator = list(self.sliding_window(v))
            score = self.evaluate(v)
            board_score += score['one'] - score['two']
        return board_score
    def choices(self):
        choices = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__board[i][j] != 0:
                    continue
                if not self.has_neighbor(i,j):
                    continue
                choices.append((i,j))
        return choices
    def new_choices(self, choice, existing_choices):
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
        additional_choices = []
        if choice is not None:
            for (xdirection, ydirection) in directions:
                if xdirection != 0 and ((choice[1] + xdirection) < 0 or (choice[1] + xdirection) >= self.__size):
                    continue
                if ydirection != 0 and ((choice[0] + ydirection) < 0 or (choice[0] + ydirection) >= self.__size):
                    continue
                if (self.__board[choice[0] + ydirection][choice[1] + xdirection] == 0) and (choice[0] + ydirection, choice[1] + xdirection) not in existing_choices:
                    additional_choices.append((choice[0] + ydirection, choice[1] + xdirection))
        return additional_choices
    def minimax(self,choices, depth, max_depth, alpha, beta, max_player, temp_choice = None, store_choice = None):
        new_choices = choices.copy()
        if max_player == 1:
            next_player = 2
        else:
            next_player = 1
        self.make_ghost_move(temp_choice, next_player)
        if depth == 0: #or win
            score = self.evaluate_board_score()
            self.remove_ghost_move(temp_choice)
            val = {'choice':store_choice, 'score':score}
            return val 
        if temp_choice is not None:
            new_choices.remove(temp_choice)
        new_choices.extend(self.new_choices(temp_choice, new_choices))
        new_choice = None
        if max_player == 1:
            maxVal = float("-inf")
            for choice in new_choices:
                if depth == max_depth:
                    store_choice = choice
                val = self.minimax(new_choices, depth - 1, max_depth, alpha, beta, 2, choice, store_choice)
                self.remove_ghost_move(temp_choice)
                if val['score'] >= maxVal:
                    maxVal = val['score']
                    new_choice = val['choice']
                alpha = max(alpha, val['score'])
                if beta <= alpha:
                    break
            return {'choice':new_choice, 'score':maxVal}
        else:
            minVal = float("inf")
            for choice in new_choices:
                val = self.minimax(new_choices, depth - 1, max_depth, alpha, beta, 1, choice, store_choice)
                if val['score'] <= minVal:
                    minVal = val['score']
                    new_choice = val['choice']
                beta = min(beta, val['score'])
                if beta <= alpha:
                    self.remove_ghost_move(temp_choice)
                    break
            self.remove_ghost_move(temp_choice)
            return {'choice':new_choice, 'score':minVal}
    def make_move(self, row, col):
        self.__board[row][col] = self.__player_turn
        self.__ghost_board = self.__board.copy()
        self.__player_turn = (self.__player_turn % 2) + 1
        self.printBoard()
    def make_ghost_move(self, choice, player_turn):
        if choice is not None:
            self.__ghost_board[choice[0]][choice[1]] = player_turn
    def remove_ghost_move(self, choice):
        if choice is not None:
            self.__ghost_board[choice[0]][choice[1]] = 0
    def choose_move(self):
        choices = self.choices()
        val = self.minimax(choices, depth=2, max_depth=2, alpha=-1000000000, beta=1000000000, max_player=1)
        return val
    def check(self):
        board = self.__board
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(self.__size):
            for j in range(self.__size):
                if board[i][j] == 0:
                    continue
                player_num = board[i][j]
                for d in dirs:
                    x, y = i, j
                    count = 0
                    for _ in range(5):
                        if self.get(x, y) != player_num:
                            break
                        x += d[0]
                        y += d[1]
                        count += 1
                    if count == 5:
                        return player_num
        return 0
    def printBoard(self):
        val = '0'
        print("")
        print("A B C D E F G H I J K L M N O", end="")
        for i in range(self.__size):
            print("")
            for j in range(self.__size):
                if self.__board[i][j] == 0:
                    val = '0'
                elif self.__board[i][j] == 1:
                    val = '1'
                elif self.__board[i][j] == 2:
                    val = '2'
                print(f"{val}", end =" ")
            print(f" {i+1}", end="")
