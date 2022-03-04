import copy
import random
from hashlib import new
from re import T


def create_empty_board():
    # create 9*9 grid populated with 0
    board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]
    return board

def print_board(board, title="Sudoku:"):
    top = "_"*27
    bottom = "‾"*27
    col_num_str = "#  0, 1, 2, 3, 4, 5, 6, 7, 8"

    print(title)
    print(col_num_str)
    print(" ", top)
    for r in range(9):
        print(r, board[r])
    print(" ", bottom)

def is_puzzle_solvable(board, brute_force=False):
    # check that there are no row collisons
    for r in range(9):
        row_vals = [val for val in board[r] if val > 0]
        if len(row_vals) != len(set(row_vals)):
            print(f"Collision detected in row [{r}]")
            return False

    # check that there are no col collisons
    for c in range(9):
        col_vals = [board[r][c] for r in range(9) if board[r][c] > 0]
        if len(col_vals) != len(set(col_vals)):
            print(f"Collision detected in column [{c}]")
            return False

    # check that there are no local block collisons
    block_start_indices = [0,3,6]

    clue_count = 0
    for block_r_start in block_start_indices:
        for block_c_start in block_start_indices:
            block = []
            for r in range(block_r_start, block_r_start + 3):
                for c in range(block_c_start, block_c_start + 3):
                    if board[r][c] != 0:
                        block.append(board[r][c])
                        clue_count += 1
            if len(block) != len(set(block)):
                print(f"Collision detected in block [{block_r_start}][{block_c_start}]")
                return False

    # check clues count >= 17, if less than 17 then attempt to solve to check if solvable
    if clue_count < 17:
        board_copy = copy.deepcopy(board)
        solvable = generate_solution(board_copy)
        return solvable
    
    if not brute_force:
        return True
    else:
        board_copy = copy.deepcopy(board)
        solvable = generate_solution(board_copy)
        return solvable

def generate_new_complete_sudoku_puzzle(board):
    # use backtracking to generate a solvable sudoku puzzle
    # game_board is a list of lists of size 9**2
    # each inner list represents a row in the game board
    # valid values: 1-9, unfilled/available spaces: 0
    # minimum number of clues to guarantee solution is 17

    valid_values = [1,2,3,4,5,6,7,8,9]
    random.shuffle(valid_values) # shuffle to try in possible values in random order

    unfilled_space = find_next_unfilled(board)
    if unfilled_space[0] == -1:
        return True
    
    for value in valid_values:
        row, col = unfilled_space

        if is_value_valid_for_space(board, value, unfilled_space):
            board[row][col] = value
            if generate_new_complete_sudoku_puzzle(board):
                return True
        else:
            board[row][col] = 0
    
    return False

def remove_numbers_from_board(board, clues_left=17):
    num_to_remove = 81-clues_left

    solvable = False
    while not solvable:
        board_copy = copy.deepcopy(board)

        # create mask
        mask = []
        while len(mask) < num_to_remove:
            i = random.randint(0,80)
            if i not in mask:
                mask.append(i)

        # apply mask
        for i in mask:
            row=i // 9
            col=i % 9
            board_copy[row][col] = 0

        solvable = is_puzzle_solvable(board=board_copy, brute_force=True)
    
    board = board_copy
    return board

def generate_new_sudoku_puzzle(board):
    generated = False
    while not generated:
        generate_new_complete_sudoku_puzzle(board)
        solvable = is_puzzle_solvable(board=board)
        if solvable:
            generated = True
    print("generated")

    board = remove_numbers_from_board(board, clues_left=27)
    print("removed numbers")
    return board

def find_next_unfilled(board):
    # find and return (row, col) for first unfilled (val==0) board space
    # if no unfilled slots return (-1, -1)

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)

    return (-1, -1)

def is_value_valid_for_space(board, value, space):
    (row, col) = space
    # check that there are no row collisons
    row_vals = [val for val in board[row] if val > 0]
    if value in row_vals:
        return False

    # check that there are no col collisons
    col_vals = [board[r][col] for r in range(9) if board[r][col] > 0]
    if value in col_vals:
        return False
    
    # check that there are no local block collisons
    block_r_start = (row // 3) * 3 # 0//3==0, 3//3=1, 8//3 = 2 etc
    block_c_start = (col // 3) * 3

    for r in range(block_r_start, block_r_start + 3):
        for c in range(block_c_start, block_c_start + 3):
            if board[r][c] == value:
                return False
    
    # returns True if no collisions, else False
    return True

def generate_solution(board):
    # use backtracking to solve sudoku puzzle
    # game_board is a list of lists of size 9**2
    # each inner list represents a row in the game board
    # valid values: 1-9, unfilled/available spaces: 0

    space = find_next_unfilled(board=board)

    # No unfilled spaces so should be solved
    if space[0] == -1:
        return True

    for value in range(1, 10):
        if is_value_valid_for_space(board, value, space):
            board[space[0]][space[1]] = value

            # use recursion to brute force the search space
            if generate_solution(board):
                return True
        elif board[space[0]][space[1]] > 0:
            board[space[0]][space[1]] = 0

    # if recursive brute force fails return False
    return False

def attempt_puzzle(board):
    print_board(board, title="Puzzle:")
    solvable = is_puzzle_solvable(board=board)
    if solvable:
        solved = generate_solution(board=board)
        if solved:
            print("Sudoku solved!!")
            print_board(board, title="Solution:")
        else:
            print("Uh Oh!! The puzzle is unsolvable")
    else:
        print("The puzzle is unsolvable")

if __name__ == '__main__':
    # from puzzles.example_puzzle_easy import puzzle as easy
    # from puzzles.example_unsolvable import puzzle as unsolvable

    # puzzles = [easy, unsolvable]

    # for puzzle in puzzles:
    #     attempt_puzzle(puzzle)

    new_board = create_empty_board()
    new_board = generate_new_sudoku_puzzle(board=new_board)
    attempt_puzzle(new_board)
