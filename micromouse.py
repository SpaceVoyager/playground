import json
import os

from cmu_graphics import *

app.stepsPerSecond = 2
app.background = 'ghostWhite'

SIZE = 20
GOAL_COLOR = 'limeGreen'
START_COLOR = 'green'
FILE_NAME = 'maze.json'
rows = 400 // SIZE
cols = 400 // SIZE
squares = {}
invisible_squares = []
presses = 0
goal_node = None
path_found = None
drawn_path_length = 0


def color_cell(current_node, color):
    squares[(current_node[0], current_node[1])].fill = color
    squares[(current_node[0], current_node[1])].visible = True
    

def is_empty(node):
    return not squares[node].visible or squares[node].fill == GOAL_COLOR
        

def find_adj_nodes(node):
    adj_nodes = []
    row, col = node
    for node in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if node in squares and is_empty(node):
            adj_nodes.append(node)
    return adj_nodes


def bfs_shortest_path(start_node, goal_node):
    queue = [(start_node, [start_node])]
    visited_nodes = set([start_node])

    while queue:
        node, path = queue.pop(0)
        for adj_node in find_adj_nodes(node):
            if adj_node not in visited_nodes:
                if adj_node == goal_node:
                    return path + [adj_node]
                visited_nodes.add(node)
                queue.append((adj_node, path + [adj_node]))
    return []


def save_maze():
    for node in squares:
        if not squares[node].visible or squares[node].fill == GOAL_COLOR or squares[node].fill == START_COLOR:
            invisible_squares.append(node)

    with open(FILE_NAME, 'w') as f:
        json.dump(invisible_squares, f)


def onStep():
    global drawn_path_length
    if path_found:
        if len(path_found) > drawn_path_length:
            color_cell(path_found[drawn_path_length], 'blue')
            drawn_path_length += 1


def onMousePress(mouseX, mouseY): 
    global presses, goal_node, path_found
    presses += 1
    print(f'presses: {presses}')
    col = mouseX // SIZE
    row = mouseY // SIZE
    if not squares[(row, col)].visible:
        if presses == 1:
            # place goal
            squares[(row, col)].visible = True
            squares[(row, col)].fill = GOAL_COLOR
            goal_node = (row, col)
        elif presses == 2:
            # place start
            squares[(row, col)].visible = True
            squares[(row, col)].fill = START_COLOR
            save_maze()
            path_found = bfs_shortest_path((row, col), goal_node)
            print('path_found:', path_found)


def onKeyPress(key):
    if (key == 'left') and cursor.left > 0:
        cursor.centerX = cursor.centerX - SIZE
    if (key == 'right') and cursor.left + SIZE < 400:
        cursor.centerX = cursor.centerX + SIZE
    if (key == 'up') and cursor.top > 0:
        cursor.centerY = cursor.centerY - SIZE
    if (key == 'down') and cursor.top + SIZE < 400:
        cursor.centerY = cursor.centerY + SIZE
    if (key =='space'):
        cursor_col = cursor.left // SIZE
        cursor_row = cursor.top // SIZE
        squares[(cursor_row, cursor_col)].visible = not squares[(cursor_row, cursor_col)].visible


if os.path.isfile(FILE_NAME):
    with open(FILE_NAME, 'r') as f:
        invisible_squares = json.load(f)
        print(f'Loaded: {invisible_squares}')

for r in range(rows):
    for c in range(cols):
        rect = Rect(c * SIZE, r * SIZE, SIZE, SIZE, fill='skyBlue', 
                    border='black', borderWidth=1)
        squares[(r, c,)] = rect

for r, c in invisible_squares:
    squares[(r, c)].visible = False 

cursor = Rect(0, 0, SIZE, SIZE, fill='red', border='black', borderWidth=1)

cmu_graphics.run()