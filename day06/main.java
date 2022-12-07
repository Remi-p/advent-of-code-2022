package day06;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

class Main {
  public static int findMarkerPosition(String elvesDataStreamBuffer, int size) {
    for (int i = 0; i < elvesDataStreamBuffer.length(); i++) {
      String section = elvesDataStreamBuffer.substring(i, i + size);
      boolean isMarker = true;
      for (char c : section.toCharArray()) {
        if (section.indexOf(c) != section.lastIndexOf(c)) {
          isMarker = false;
          break;
        }
      }
      if (isMarker) {
        return i + size;
      }
    }
    return -1;
  }

  public static void main(String[] s) throws FileNotFoundException, IOException {
    File adventInput = new File("./day06/input.txt");
    Scanner reader = new Scanner(adventInput);

    String elvesDataStreamBuffer = reader.nextLine();
    System.out.println("Marker position: " + Main.findMarkerPosition(elvesDataStreamBuffer, 4));
    System.out.println("Message marker position: " + Main.findMarkerPosition(elvesDataStreamBuffer, 14));

    reader.close();
  }
}