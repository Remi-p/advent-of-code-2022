package day07;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

class Main {
  public static void main(String[] s) throws FileNotFoundException, IOException {
    CommandLineParser parser = new CommandLineParser(Files.readString(Path.of("./day07/input.txt")));
    ItemsRepository repository = parser.constructRepository();
    System.out.println(repository);

    System.out.println("Size:");
    System.out.println(repository.getSize());

    System.out.println("Sum of folders at most 100000");
    System.out.println(repository.sumDirectoriesSizeUnder(100000));

    System.out.println("------------");
    int TOTAL_SPACE = 70000000;
    int spaceToGain = (30000000 - (TOTAL_SPACE - repository.getSize()));
    System.out.println("Size needed to be freed: " + spaceToGain);

    System.out.println("Repository size to delete:");
    System.out.println(repository.getSmallestDirectoryGreaterThan(spaceToGain, TOTAL_SPACE));
  }
}

enum ItemType {
  FILE,
  FOLDER
}

class ItemsRepository {
  String name;
  ItemType type;
  private int size = 0;
  HashMap<String, ItemsRepository> contents = new HashMap<>();

  public int getSize() {
    if (this.size != 0) {
      return size;
    }
    int size = 0;
    for (Map.Entry<String, ItemsRepository> set : this.contents.entrySet()) {
      size += set.getValue().getSize();
    }
    return size;
  }

  public void setSize(int size) {
    this.size = size;
  }

  public boolean isFolder() {
    return this.type == ItemType.FOLDER;
  }

  ItemsRepository(String name, ItemType type) {
    this.name = name;
    this.type = type;
  }

  void addItem(ItemsRepository item, Stack<String> path) {
    path.remove(0);
    if (path.size() == 0) {
      // System.out.println("Add element " + item + " inside " + this.name);
      this.contents.put(item.name, item);
      return;
    }
    this.contents.get(path.get(0)).addItem(item, path);
  }

  public String toString() {
    String current = "(" + this.getSize() + ") " + this.type + " " + this.name;
    if (this.contents.size() == 0) {
      return current;
    }
    return current + ": " + this.contents;
  }

  public int sumDirectoriesSizeUnder(int sizeMax) {
    int total = 0;
    for (Map.Entry<String, ItemsRepository> set : this.contents.entrySet()) {
      total += set.getValue().sumDirectoriesSizeUnder(sizeMax);
    }
    if (this.isFolder() && this.getSize() <= sizeMax) {
      total += this.getSize();
    }
    return total;
  }

  public int getSmallestDirectoryGreaterThan(int spaceToGain, int lastFoundRepositorySize) {
    for (Map.Entry<String, ItemsRepository> set : this.contents.entrySet()) {
      lastFoundRepositorySize = set.getValue().getSmallestDirectoryGreaterThan(spaceToGain, lastFoundRepositorySize);
    }
    if (this.isFolder() && this.getSize() >= spaceToGain && this.getSize() <= lastFoundRepositorySize) {
      return this.getSize();
    }
    return lastFoundRepositorySize;
  }
}

class CommandLineParser {
  String[] commands;
  Stack<String> currentDirectory;
  ItemsRepository repository;

  CommandLineParser(String input) {
    this.commands = input.split("\\$");
    this.goToRoot();
  }

  private void goToRoot() {
    this.currentDirectory = new Stack<>();
    this.currentDirectory.push("/");
  }

  private void cd(String direction) {
    switch (direction) {
      case "/":
        this.goToRoot();
        break;
      case "..":
        this.currentDirectory.pop();
        break;
      default:
        this.currentDirectory.add(direction);
        break;
    }
    // System.out.println("currentDir=>" + this.currentDirectory);
  }

  private void ls(String[] commandOutput) {
    for (int i = 1; i < commandOutput.length; i++) {
      String[] itemInput = commandOutput[i].split(" ");
      ItemsRepository item;
      switch (itemInput[0]) {
        case "dir":
          item = new ItemsRepository(itemInput[1], ItemType.FOLDER);
          break;
        default:
          item = new ItemsRepository(itemInput[1], ItemType.FILE);
          item.setSize(Integer.parseInt(itemInput[0]));
          break;
      }
      this.repository.addItem(item, (Stack) this.currentDirectory.clone());
    }
  }

  public ItemsRepository constructRepository() {
    this.repository = new ItemsRepository("/", ItemType.FOLDER);

    for (int i = 1; i < commands.length; i++) {
      String[] lines = commands[i].split("\n");
      String[] command = lines[0].split(" ");
      switch (command[1]) {
        case "cd":
          this.cd(command[2]);
          break;
        case "ls":
          this.ls(lines);
          break;
      }
    }
    return this.repository;
  }
}