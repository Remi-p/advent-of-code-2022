import sys
import logging

with open("./day01/input.txt") as text_input:
  elves=[0]
  for line in text_input:
    if (line == "\n"):
      elves.append(0)
      continue
    elves[-1] = elves[-1] + int(line)
  
  elves.sort(reverse=True)
  
  most = elves[0]
  print("Most:" + str(most))

  top_three = elves[0] + elves[1] + elves[2]
  print("Top three:" + str(top_three))

  # max_elve = -1
  # max_cal = 0
  # for (i, elve) in enumerate(elves):
  #   print("Elve #" + str(i+1) + ", cal: " + str(elve))
  #   if (max_cal < elve):
  #     max_elve = i +1
  #     max_cal = elve
    
  # print(max_elve)
  # print(max_cal)