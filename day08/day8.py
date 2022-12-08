import sys
import logging

def isTreeVisible(height: int, x: int, y: int, tree_line: "list[int]", tree_column: "list[int]"):
  # print(x,y, tree_line[:x], tree_line[x], tree_line[x+1:], tree_column[:y], tree_column[y], tree_column[y+1:])
  return (
    height > max(tree_line[:x]) or
    height > max(tree_line[x+1:]) or
    height > max(tree_column[:y]) or
    height > max(tree_column[y+1:]))

def getViewingDistance(fromHeight: int, trees: "list[int]"):
  treesGreaterOrEqual = [idx for idx, val in enumerate(trees) if val >= fromHeight]
  if (len(treesGreaterOrEqual) == 0):
    return len(trees)
  return treesGreaterOrEqual[0] + 1

def getTreeScenicScore(height: int, x: int, y: int, tree_line: "list[int]", tree_column: "list[int]"):
  # if (x == 2 and y == 3):
  #   print(x,y, tree_line[:x], tree_line[x], tree_line[x+1:], tree_column[:y], tree_column[y], tree_column[y+1:])

  return (
    getViewingDistance(height, list(reversed(tree_line[:x]))) *
    getViewingDistance(height, tree_line[x+1:]) *
    getViewingDistance(height, list(reversed(tree_column[:y]))) *
    getViewingDistance(height, tree_column[y+1:])
  )

with open("./day08/input.txt") as text_input:
  trees=[]

  for line in text_input:
    trees_column = [int(tree) for tree in line.strip()]
    trees.append(trees_column)

  line_length = len(trees[0])
  column_length = len(trees)

  total_visible_trees = (line_length + column_length) * 2 - 4
  highest_scenic_score = 0
  
  for y in range(1, line_length - 1):
    for x in range(1, column_length - 1):
      tree_line = trees[y]
      tree_column = [line[x] for line in trees]

      if isTreeVisible(trees[y][x], x, y, tree_line, tree_column):
        total_visible_trees += 1
      
      scenic_score = getTreeScenicScore(trees[y][x], x, y, tree_line, tree_column)

      if (scenic_score > highest_scenic_score):
        highest_scenic_score = scenic_score
      
  print(line_length)
  print(column_length)
  print("Visible trees: "+str(total_visible_trees))

  print("Highest scenic score: " + str(highest_scenic_score))