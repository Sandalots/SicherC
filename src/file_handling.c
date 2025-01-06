#include <stdio.h>

int line = 0;
int pos = 0;

int get_lines(FILE *fp) {
  int count = 0;
  char c;

  if (fp == NULL) {
    printf("Could not open file.\n");
    return 1;
  }

  while ((c = fgetc(fp)) != EOF) {
    if (c == '\n') {
      count ++;
    }
  }

  rewind(fp);
  return count;
}
