import sys
def read_sudoku(file):
    size = int(file.readline())
    n_full_cells = int(file.readline())
    grid = [[0] * size for _ in range(size)]
    for _ in range(n_full_cells):
        i, j, value = map(int, file.readline().split())
        grid[i][j] = value
    return grid

def print_sudoku(grid):
    for row in grid:
        print(' '.join(str(cell) for cell in row))

def is_valid(grid, size, row, col, num):
    for i in range(size):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    box_size = int(size ** 0.5)
    box_row, box_col = row // box_size * box_size, col // box_size * box_size
    for i in range(box_size):
        for j in range(box_size):
            if grid[box_row + i][box_col + j] == num:
                return False
    return True

def find_unassigned(grid, size):
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                return row, col
    return None

def mrv(grid, size):
    min_remaining, min_pos = sys.maxsize, None
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                count = sum(is_valid(grid, size, row, col, num) for num in range(1, size + 1))
                if count < min_remaining:
                    min_remaining, min_pos = count, (row, col)
    return min_pos

def lcv(grid, size, row, col):
    return sorted((num for num in range(1, size + 1) if is_valid(grid, size, row, col, num)),
                  key=lambda num: sum(is_valid(grid, size, row, col, num) for row in range(size) for col in range(size)))

def ac3(grid, size, queue):
    while queue:
        row, col = queue.pop(0)
        if revise(grid, size, row, col):
            if grid[row][col] == 0:
                return False
            for i in range(size):
                if i != col and grid[row][i] == 0:
                    queue.append((row, i))
                if i != row and grid[i][col] == 0:
                    queue.append((i, col))
            box_size = int(size ** 0.5)
            box_row, box_col = row // box_size * box_size, col // box_size * box_size
            for i in range(box_size):
                for j in range(box_size):
                    r, c = box_row + i, box_col + j
                    if r != row and c != col and grid[r][c] == 0:
                        queue.append((r, c))
    return True

def revise(grid, size, row, col):
    revised = False
    for num in range(1, size + 1):
        if grid[row][col] == num:
            continue
        if not is_valid(grid, size, row, col, num):
            grid[row][col] = 0
            revised = True
            break
    return revised

def solve_sudoku(grid, size):
    queue = [(row, col) for row in range(size) for col in range(size) if grid[row][col] == 0]
    ac3(grid, size, queue)
    unassigned = mrv(grid, size)
    if unassigned is None:
        return True
    row, col = unassigned
    for num in lcv(grid, size, row, col):
        if is_valid(grid, size, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid, size):
                return True
            grid[row][col] = 0
    return False

if __name__ == '__main__':
    with open('/Users/omid/Downloads/input25.txt', 'r') as file:
        grid = read_sudoku(file)
    size = len(grid)
    if solve_sudoku(grid, size):
        print_sudoku(grid)
    else:
        print('Unsolvable CSP!')