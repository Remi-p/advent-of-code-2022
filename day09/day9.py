import sys
import logging

def sign(i: int):
  return 1 if i < 0 else -1

class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def distanceX(self, pos: "Position"):
    return abs(pos.x - self.x)
  def distanceY(self, pos: "Position"):
    return abs(pos.y - self.y)
  def targetDirectionX(self, pos: "Position"):
    return sign(pos.x - self.x)
  def targetDirectionY(self, pos: "Position"):
    return sign(pos.y - self.y)
  def stringifiedPos(self):
    return str(self.x) + "-" + str(self.y);

class RopeEnd(Position):
  def isInPos(self, x: int, y: int):
    return (self.x == x and self.y == y)
  def move(self, direction: str):
    switch={
      "R": Position(+1, 0),
      "L": Position(-1, 0),
      "U": Position(0, +1),
      "D": Position(0, -1)
    }
    moves = switch.get(direction)
    self.x += moves.x
    self.y += moves.y
  def follow(self, ropeEnd: "RopeEnd"):
    if (self.distanceX(ropeEnd) * self.distanceY(ropeEnd) > 1):
      self.x -= self.targetDirectionX(ropeEnd)
      self.y -= self.targetDirectionY(ropeEnd)
      return
    if (self.distanceX(ropeEnd) > 1):
      self.x -= self.targetDirectionX(ropeEnd)
    if (self.distanceY(ropeEnd) > 1):
      self.y -= self.targetDirectionY(ropeEnd)
    

def printGrid(head: RopeEnd, tail: RopeEnd):
  SIZE = 6
  print('-' * SIZE)
  for y in reversed(range(0, SIZE)):
    for x in range(0, SIZE):
      if (head.isInPos(x, y)):
        print("H", end="")
      elif (tail.isInPos(x, y)):
        print("T", end="")
      else:
        print("·", end="")
    print()

def day1(text_input):
  head = RopeEnd(0, 0)
  tail = RopeEnd(0, 0)
  tail_positions = {}
  for line in text_input:
    [direction, times] = line.strip().split(" ")
    for i in range(int(times)):
      head.move(direction)
      tail.follow(head)
      tail_positions[tail.stringifiedPos()] = True
      # printGrid(head, tail)

  tail_positions_visited_count = len(tail_positions)

  print(str(tail_positions_visited_count) + " positions were visited by the tail")

def day2(text_input, knots_count: int):
  head = RopeEnd(0, 0)
  knots = [RopeEnd(0, 0) for i in range(knots_count)] 
  tail_positions = {}
  for line in text_input:
    [direction, times] = line.strip().split(" ")
    for i in range(int(times)):
      head.move(direction)
      knots[0].follow(head)
      for i in range(1, knots_count):
        knots[i].follow(knots[i-1])
      tail_positions[knots[-1].stringifiedPos()] = True
      # printGrid(head, knots[-1])

  tail_positions_visited_count = len(tail_positions)

  print(str(tail_positions_visited_count) + " positions were visited by the tail")

with open("./day09/input.txt") as text_input:
  # day1(text_input)
  day2(text_input, 9)
