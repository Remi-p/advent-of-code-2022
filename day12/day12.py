

class Position:
  x: int
  y: int
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
  def __str__(self) -> str:
    return "[" + str(self.x) + ", " + str(self.y) + "]"

class Cell(Position):
  height: int
  distance_from_start: int
  def __init__(self, height: int):
    self.height = height
    self.distance_from_start = -1

class Grid:
  grid: "list[list[Cell]]"
  x_len: int
  y_len: int
  climbing: bool
  def __init__(self, grid: "list[list[Cell]]", climbing: bool):
    self.grid = grid
    self.x_len = len(grid[0])
    self.y_len = len(grid)
    self.climbing = climbing
  def set(self, position: Position, cell: Cell):
    self.grid[position.y][position.x] = cell
  def setXY(self, x: int, y: int, cell: Cell):
    self.grid[y][x] = cell
  def get(self, position: Position):
    return self.grid[position.y][position.x]
  def getXY(self, x: int, y: int):
    return self.grid[y][x]
  def getDistanceXY(self, x: int, y: int):
    return self.getXY(x, y).distance_from_start
  def getDistance(self, pos: Position):
    return self.get(pos).distance_from_start
  def setDistanceXY(self, x: int, y: int, distance: int):
    self.getXY(x, y).distance_from_start = distance
  def setDistance(self, pos: Position, distance: int):
    self.get(pos).distance_from_start = distance
  def getHeightXY(self, x: int, y: int):
    return self.getXY(x, y).height
  def getHeight(self, pos: Position):
    return self.get(pos).height
  def printGrid(self):
    print('-' * self.x_len)
    for y in range(0, self.y_len):
      for x in range(0, self.x_len):
        str_to_display: str
        if (self.getDistanceXY(x, y) == -1):
          str_to_display = "N-A"
        else:
          str_to_display = "{0:03}".format(self.getDistanceXY(x, y))
        print(str_to_display + "·", end="")
      print()
  def canGoTo(self, initial_position: Position, goal: Position):
    current_height = self.getHeight(initial_position)
    x = goal.x
    y = goal.y
    if (x < 0 or y < 0 or x > self.x_len - 1 or y > self.y_len - 1):
      return False
    goal_height = self.getHeight(goal)
    if (self.climbing == True):
      return (self.getDistance(goal) == -1 and goal_height <= current_height + 1);
    else:
      return (self.getDistance(goal) == -1 and goal_height >= current_height - 1);
  def expand(self, current_position: Position, distance_from_start: int):
    directions = [Position(-1, 0), Position(1, 0), Position(0, -1), Position(0, 1)]

    for direction in directions:
      goal = Position(
        current_position.x + direction.x,
        current_position.y + direction.y
      )
      if self.canGoTo(current_position, goal):
        self.setDistance(goal, distance_from_start + 1)
  def travel(self, distance_from_start: int, goal: Position = None):
    actual_distance_count = 0
    for y in range(self.y_len):
      for x in range(self.x_len):
        if (self.getDistanceXY(x, y) == distance_from_start):
          actual_distance_count += 1
          self.expand(Position(x, y), distance_from_start)
    if (actual_distance_count == 0):
      print("(Travelling was blocked at distance " + str(distance_from_start) + ")")
      return
    # self.printGrid()
    self.travel(distance_from_start + 1, goal)
  def findSmallestDistanceForHeight(self, searched_height: int):
    smallest_distance = self.y_len * self.x_len
    for y in range(self.y_len):
      for x in range(self.x_len):
        height = self.getHeightXY(x, y)
        if (height == searched_height
          and self.getDistanceXY(x, y) != -1
          and self.getDistanceXY(x, y) <= smallest_distance):
          smallest_distance = self.getDistanceXY(x, y)
    return smallest_distance

def day1(grid_array: "list[list[int]]", starting_point: Position, ending_point: Position):
  grid = Grid(grid_array, True)
  grid.set(starting_point, Cell(1))
  grid.setDistance(starting_point, 0)
  grid.get(ending_point).height = ord('z') - 96
  
  grid.travel(0, ending_point)

  print("Total steps to achieve goal: " + str(grid.getDistance(ending_point)))

def day2(grid_array: "list[list[int]]", starting_point: Position):
  grid = Grid(grid_array, False)
  grid.setDistance(starting_point, 0)
  grid.get(starting_point).height = ord('z') - 96
  
  grid.travel(0)

  print("Smallest distance hike: " + str(grid.findSmallestDistanceForHeight(ord('a') - 96)))

with open("./day12/input.txt") as text_input:
  grid_array=[]

  starting_point: Position
  ending_point: Position

  for line in text_input:
    grid_line = [Cell(ord(char) - 96) for char in line.strip()]
    grid_array.append(grid_line)
    if ('S' in line.strip()):
      starting_point = Position(line.strip().index('S'), len(grid_array) - 1)
    if ('E' in line.strip()):
      ending_point = Position(line.strip().index('E'), len(grid_array) - 1)

  # day1(grid_array, starting_point, ending_point)
  day2(grid_array, ending_point)