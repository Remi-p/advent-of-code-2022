#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// https://www.programmingsimplified.com/c/source-code/c-substring
void substring(char s[], char * sub, int start, int end) {
  int c = 0;

  while (c < end - start) {
    sub[c] = s[start+c-1];
    c++;
  }
  sub[c] = '\0';
}

int signalstrength(int X, int *cycle_number, int *signal_strength) {
  if ((*cycle_number + 20) % 40 == 0) {
    // printf("X=%i,%ith\n", X, *cycle_number);
    *signal_strength += *cycle_number * X;
  }
}

void crtdrawing(int X, int *cycle_number, int *signal_strength) {
  int crt_position = (*cycle_number-1) % 40;
  if (crt_position % 40 == 0) {
    printf("\n");
  }
  if (X - 1 <= crt_position && X + 1 >= crt_position) {
    // printf("X=%i,%ith\n", X, *cycle_number);
    printf("#");
  } else {
    printf("·");
  }
}

int docycle(int X, int *cycle_number, int *signal_strength) {
  signalstrength(X, cycle_number, signal_strength);
  crtdrawing(X, cycle_number, signal_strength);
  *cycle_number += 1;
}

int main(void)
{
    FILE * fp;
    char * line = NULL;
    char sub[10];
    size_t len = 0;
    ssize_t read;

    // https://stackoverflow.com/a/3501681
    fp = fopen("./day10/input.txt", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    
    int X = 1;
    int cycles = 1;
    int signal_strength = 0;

    while ((read = getline(&line, &len, fp)) != -1) {
        // printf("%s", line);
        if (line[0] == 'a') {
          docycle(X, &cycles, &signal_strength);
          docycle(X, &cycles, &signal_strength);
          substring(line, sub, 6, strlen(line));
          X += atoi(sub);
        } else {
          docycle(X, &cycles, &signal_strength);
        }
    }

    printf("\nSignal strength=%i\n", signal_strength);

    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}