import numpy as np
import time
import cv2

def draw_life_board(board, cell_size=5,cell_color=(255,0,0)):

    n_rows, n_cols = board.shape

    im_width = n_cols*cell_size+(n_cols+1)
    im_height = n_rows*cell_size+(n_rows+1)

    img = np.zeros((im_height,im_width,3), np.uint8)

    color=(50,50,50)
    for row in range(0,im_height,cell_size+1):
        cv2.line(img, (0,row), (im_width-1,row), color, 1)


    for col in range(0,im_width,cell_size+1):
        cv2.line(img, (col,0), (col,im_height-1), color, 1)

    for col in range(board.shape[1]):
        for row in range(board.shape[0]):
            if board[row,col] > 0:
                left_col = col*cell_size + col + 1
                right_col = left_col + cell_size - 1
                top_row = row*cell_size + row + 1
                bot_row = top_row + cell_size - 1
                img = cv2.rectangle(img, (left_col,top_row), (right_col,bot_row), cell_color, -1)

    return img


def init_life(file_name):
    f = open(file_name,'r')
    file = f.read()
    lines = file.split('\n')

    n_cols = len(lines[0])
    n_rows = 0

    for i, line in enumerate(lines):
        if len(line) != n_cols:
            break
        n_rows += 1

    A = np.zeros((n_rows,n_cols), dtype=np.int8)
    for row in range(n_rows):
        for col in range(n_cols):
            if lines[row][col] == 'X':
                A[row,col] = 1
    return A

def allive_cells (ground, row, col):
    number = 0
    num_rows, num_cols = ground.shape
    for a,b in [(1,0),(0,1),(-1,0),(0,-1)]:
          if row + a >= 0 and col + b >= 0 and row + a < num_rows and col + b < num_cols:
               number += ground[row+a, col+b]
    return number
        

def life(ground):
    new_ground = np.zeros(ground.shape, dtype=np.int8)
    num_rows, num_cols = ground.shape

    for row in range(num_rows):
        for col in range(num_cols):
            n_allive_cells = allive_cells(ground, row, col)
            if ground[row,col] == 1:
                if n_allive_cells == 2 or n_allive_cells == 3:
                    new_ground[row,col] = 1
                else:
                    new_ground[row,col] = 0
            else:
                if n_allive_cells == 3:
                    new_ground[row,col] = 1

    return new_ground       


if __name__ == "__main__":

    battle_ground = init_life('init2.txt')
    print(battle_ground)
    print()
    print()

    n_epoch = 0
    img_array = []
    while True:
        n_epoch += 1
        new_battle_ground = life(battle_ground)
        n_changes = np.sum(new_battle_ground != battle_ground )
        if n_changes == 0:
            for i in range(10):
                img_array.append(img)
            break

        img = draw_life_board(new_battle_ground, cell_size=50, cell_color=(0,255,0))
        img_array.append(img)

        print("epoch:", n_epoch,"#changes:", n_changes)
        print(new_battle_ground)
        print()
        print()
        battle_ground = new_battle_ground
        time.sleep(0.5)

    print("#epochs:", n_epoch)

    height, width, layers = img.shape
    size = (width,height)

    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()