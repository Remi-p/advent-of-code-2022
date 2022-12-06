package day04;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;
import java.util.Scanner;

class Main {
  public static void main(String[] s) throws FileNotFoundException, IOException {
    File adventInput = new File("./day04/input.txt");
    Scanner reader = new Scanner(adventInput);

    int totalContained = 0;
    int totalOverlap = 0;

    while (reader.hasNextLine()) {
      ElvesPair elves = new ElvesPair(reader.nextLine());
      if (elves.doesOneContainsTheOther()) {
        totalContained += 1;
      }
      if (elves.doTheyOverlap()) {
        totalOverlap += 1;
      }
    }

    System.out.println("Total contained = " + totalContained);
    System.out.println("Total overlapped = " + totalOverlap);
    reader.close();
  }
}

class ElvesPair {
  int[] elf1;
  int[] elf2;

  ElvesPair(String stringifiedElves) {
    String[] elves = stringifiedElves.split(",");
    this.elf1 = Arrays.stream(elves[0].split("-")).mapToInt(Integer::parseInt).toArray();
    this.elf2 = Arrays.stream(elves[1].split("-")).mapToInt(Integer::parseInt).toArray();
  }

  boolean doesOneContainsTheOther() {
    return (this.elf1[0] >= this.elf2[0] && this.elf1[1] <= this.elf2[1])
        || (this.elf1[0] <= this.elf2[0] && this.elf1[1] >= this.elf2[1]);
  }

  boolean doTheyOverlap() {
    return (this.elf1[0] >= this.elf2[0] && this.elf1[0] <= this.elf2[1])
        || (this.elf1[1] >= this.elf2[0] && this.elf1[1] <= this.elf2[1])
        || (this.elf2[0] >= this.elf1[0] && this.elf2[0] <= this.elf1[1])
        || (this.elf2[1] >= this.elf1[0] && this.elf2[1] <= this.elf1[1]);
  }
}