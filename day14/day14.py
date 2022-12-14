import enum

class BlockType(enum.Enum):
   RestedSand = 1
   Block = 2

class Position:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
  def __str__(self) -> str:
    return "[" + str(self.x) + ", " + str(self.y) + "]"

class Grid:
  blocks: "dict[str, BlockType]"
  animated_sand: "Position | None"
  x_start: "int | None" = None
  x_end: "int | None" = None
  y_start: "int | None" = None
  y_end: "int | None" = None
  def __init__(self):
    self.blocks = {}
  def computeBorders(self, pos: Position):
    if (self.x_start == None):
      self.x_start = pos.x
      self.y_start = pos.y
      self.x_end = pos.x
      self.y_end = pos.y
    if (self.x_start > pos.x):
      self.x_start = pos.x
    if (self.x_end < pos.x):
      self.x_end = pos.x
    if (self.y_start > pos.y):
      self.y_start = pos.y
    if (self.y_end < pos.y):
      self.y_end = pos.y + 1
  def parseInput(self, input_text: str):
    for block_line in input_text:
      points = block_line.strip().split(" -> ")
      for i in range(len(points) - 1):
        [point_a_x, point_a_y] = map(int, points[i].split(","))
        [point_b_x, point_b_y] = map(int, points[i+1].split(","))
        self.computeBorders(Position(point_a_x, point_a_y))
        self.computeBorders(Position(point_b_x, point_b_y))
        if (point_a_x + point_a_y > point_b_x + point_b_y):
          [x_goal, y_goal] = [point_a_x, point_a_y]
          [x_source, y_source] = [point_b_x, point_b_y]
        else:
          [x_goal, y_goal] = [point_b_x, point_b_y]
          [x_source, y_source] = [point_a_x, point_a_y]
        for x in range(x_source, x_goal + 1):
          for y in range(y_source, y_goal + 1):
            self.set(Position(x, y), BlockType.Block)
  def addSand(self, position: Position):
    self.animated_sand = position
    self.computeBorders(position)
  def set(self, position: Position, block: BlockType):
    self.blocks[str(position)] = block
  def get(self, position: Position):
    if (str(position) in self.blocks):
      return self.blocks[str(position)]
    else:
      return None
  def countSandBlocks(self):
    count = 0
    for idx in self.blocks:
      if (self.blocks[idx] == BlockType.RestedSand):
        count += 1
    return count
  def printGrid(self):
    print('=' * (self.x_end - self.x_start + 1))
    for y in range(self.y_start, self.y_end + 1):
      for x in range(self.x_start, self.x_end + 1):
        if (self.get(Position(x, y)) == BlockType.Block):
          print("█", end="")
        elif (self.get(Position(x, y)) == BlockType.RestedSand):
          print("▓", end="")
        elif (str(self.animated_sand) == str(Position(x, y))):
          print("░", end="")
        else:
          print("·", end="")
      print()
  def animate(self):
    while self.animated_sand != None:
      x = self.animated_sand.x
      y = self.animated_sand.y
      if (self.get(Position(x, y)) != None):
        return False
      # =========================== Part #1:
      # elif (y >= self.y_end):
      #   return False
      # =========================== Part #2:
      elif (y >= self.y_end):
        self.set(Position(x, y), BlockType.RestedSand)
        self.animated_sand = None
        return True
      if (self.get(Position(x, y+1)) == None):
        self.animated_sand = Position(x, y + 1)
      elif (self.get(Position(x-1, y+1)) == None):
        self.animated_sand = Position(x - 1, y + 1)
      elif (self.get(Position(x+1, y+1)) == None):
        self.animated_sand = Position(x + 1, y + 1)
      else:
        self.set(Position(x, y), BlockType.RestedSand)
        self.animated_sand = None
        return True
      # self.printGrid()
    return False

with open("./day14/input.txt") as text_input:
  grid = Grid()
  grid.parseInput(text_input)
  
  grid.addSand(Position(500, 0))
  while grid.animate():
    grid.addSand(Position(500, 0))
  
  grid.printGrid()

  print(str(grid.countSandBlocks()))