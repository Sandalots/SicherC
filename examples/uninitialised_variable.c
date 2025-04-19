/* Description: A Simple C Program that initialises a variable
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdio.h>

// Uninitialised Variable Test
int main() {
    // define a uninitialised variable
    int oneWithoutValue;

    // I will also define a variable that goes unusued in the program
    int unusedVariable = 0;

    // Let's output the value of the uninitialised variable, note the formatting
    printf("Let's see what the totally real value of oneWithoutValue is!: %d\n", oneWithoutValue);

    // end of the program
    return 0;
}