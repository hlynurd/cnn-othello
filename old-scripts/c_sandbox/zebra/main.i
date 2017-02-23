/* example.i */
%module example
%{
/* Put header files here or function declarations like below */
#include <stdio.h>
#include "constant.h"
#include "globals.h"
#include "game.h"
#include "bitboard.h"
#include "stable.h"
#include "moves.h"
extern int main(void);
%}

extern int main(void);
