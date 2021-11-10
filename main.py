import numpy as np
import math
import copy
import time
from queue import PriorityQueue as pq


def swap(puzzle, x1, y1, x2, y2):
    temp = puzzle.Numbers[x1][y1]
    puzzle.Numbers[x1][y1] = puzzle.Numbers[x2][y2]
    puzzle.Numbers[x2][y2] = temp


class Puzzle:
    Numbers = np.random.choice(np.arange(9), size=9, replace=False)
    #[[1, 4, 2], [3, 7, 5], [6, 8, 0]]
    #  1 4 2
    #  3 7 5
    #  6 8 0
    # np.random.choice(np.arange(9), size=9, replace=False)

    def __init__(self):
        self.shuffle()

    def get_space(self):
        for i in range(0, len(self.Numbers)):
            for j in range(0, len(self.Numbers[i])):
                if self.Numbers[i][j] == 0:
                    return i, j

    def print_puzzle(self):
        print(str(self.Numbers[0][0]) + "|" + str(self.Numbers[0][1]) + "|" + str(self.Numbers[0][2]))
        print("-----")
        print(str(self.Numbers[1][0]) + "|" + str(self.Numbers[1][1]) + "|" + str(self.Numbers[1][2]))
        print("-----")
        print(str(self.Numbers[2][0]) + "|" + str(self.Numbers[2][1]) + "|" + str(self.Numbers[2][2]))

    def is_solvable(self):
        cnt = 0
        for i in range(8):
            for j in range(i+1,8):
                if self.Numbers[math.floor(j/3)][j%3] > self.Numbers[math.floor(i/3)][i%3]: cnt += 1
        return cnt % 2 == 0

    def to_string(self):
        s = ""
        for i in self.Numbers:
            for j in i : s += str(j)
        return s

    def shuffle(self):
        while True :
            self.Numbers = np.random.choice(np.arange(9), size=9, replace=False)
            self.Numbers = self.Numbers.reshape(3,3)
            if self.is_solvable() : break

    def move(self, dir):
        new_puzzle = Puzzle()
        new_puzzle.Numbers = copy.deepcopy(self.Numbers)
        x, y = self.get_space()
        if dir == 'S' and x < 2:
            swap(new_puzzle, x, y, x + 1, y)
        elif dir == 'N' and x > 0:
            swap(new_puzzle, x, y, x - 1, y)
        elif dir == 'E' and y < 2:
            swap(new_puzzle, x, y, x, y + 1)
        elif dir == 'W' and y > 0:
            swap(new_puzzle, x, y, x, y - 1)
        else:
            return -1
        return new_puzzle

    def goal_achived(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.Numbers[i][j] != i * 3 + j: return False
        return True

    def heuristics(self):
        answer = 0
        for i in range(0, 3):
            for j in range(0, 3):
                y = abs(j - (self.Numbers[i][j] % 3))
                x = abs(i - math.floor(self.Numbers[i][j] / 3))
                answer += x + y
        return answer

    def f(self,depth):
        return self.heuristics()+depth

    def __gt__(self, puzzle):
        if (self.heuristics()) > (puzzle.heuristics()):
            return True
        else:
            return False


class Solve:
    puzzle = Puzzle()

    def __init__(self):
        pass

    def arraw(self):
        print(" | |")
        print(" | |")
        print(" \ / ")

    def Astar(self):
        heap = pq()
        moves = ['N', 'E', 'W', 'S']
        front = [self.puzzle.f(0) ,self.puzzle, 0]
        heap.put(front)
        puzzle_set = {front[1].to_string()}
        itr = 0
        tic = time.time()
        while front and front[1].goal_achived() != True:
            front = heap.get()
            itr += 1
            self.arraw()
            front[1].print_puzzle()
            print("At Depth :"+str(front[2]) + ", F(n) = " + str(front[1].heuristics()+front[2]))
            print("The Number of Iterations : "+str(itr))
            toc = time.time()
            if toc - tic > 60*5 :
                print("time over five minutes passed ")
                break
            for i in moves:
                new_puzzle = front[1].move(i)
                if new_puzzle != -1:
                    if new_puzzle.to_string() in puzzle_set : continue
                    puzzle_set.add(new_puzzle.to_string())
                    heap.put([new_puzzle.f(front[2] + 1), new_puzzle, front[2] + 1])
            if front[2] == 181440:
                print("Sorry the puzzle is unsolvable try again")
                return front[1]
        return front[1]


solve = Solve()

while True:
    auto_man = input("If you want to insert the game press M or make a random game press R or Z to Exit\n")

    while auto_man != 'M' and auto_man !='R' and auto_man != 'Z':
        auto_man = input("If you want to insert the game press M or make a random game press R or Z to Exit\n")
    # 7 1 2
    # 5 0 6        this puzzle for exaple takes 1660 iteration for solving it
    # 8 3 4
    if auto_man == 'M':
        print("Insert values sequentially : ")
        Numbers = np.random.choice(np.arange(9), size=9, replace=False)
        for i in range(9) : Numbers[i] = input()
        solve.puzzle.Numbers = Numbers.reshape(3,3)
        solve.puzzle.print_puzzle()

    elif auto_man == 'R' : solve.puzzle.shuffle()

    elif auto_man == 'Z': break

    if solve.puzzle.is_solvable() == False :
        print("Sorry the puzzle is unsolvable try again")
        continue
    solve.Astar()