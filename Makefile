CC=gcc
CXX=g++

CFLAGS=-Wall -Wextra -pedantic -std=c99 -Iinclude 
CXXFLAGS=-Wall -Wextra -pedantic -std=c++11 -Iinclude 

SRC_DIR=src
INC_DIR=include
TESTS_DIR=tests

SRC=$(wildcard $(SRC_DIR)/*.c)
OBJ_SRC=$(SRC:.c=.o)

TESTS_SRC=$(wildcard $(TESTS_DIR)/*.c)
OBJ_TESTS=$(TESTS_SRC:.c=.o)

all: main

main: $(OBJ_SRC) 
	$(CC) $(OBJ_SRC) -o sicher

$(OBJ_SRC): %.o : %.c 
	$(CC) $(CFLAGS) -c $< -o $@


clean:
	rm -rf $(OBJ_SRC) $(OBJ_TESTS) sicher
