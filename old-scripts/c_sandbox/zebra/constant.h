/*
   File:         constant.h

   Created:      July 10, 1997

   Modified:     September 14, 2002

   Author:       Gunnar Andersson (gunnar@radagast.se)

   Contents:     Some globally used constants.
*/



#ifndef CONSTANT_H
#define CONSTANT_H



#ifdef __cplusplus
extern "C" {
#endif



/* Symbolic values for the possible contents of a square */
#define ILLEGAL                     -3
#define BLACKSQ                     -1
#define EMPTY                       0
#define WHITESQ                     1
#define OUTSIDE                     3

#define OPP( color )                ((BLACKSQ + WHITESQ) - (color))

/* Some default values for the interface */
#define DEFAULT_WAIT                0
#define DEFAULT_ECHO                1
#define DEFAULT_DISPLAY_PV          1

/* Miscellaneous */
#define MAX_SEARCH_DEPTH            64
#define PASS                        -1
#define SEARCH_ABORT                -27000

#ifndef TRUE
#define TRUE                        1
#endif

#ifndef FALSE
#define FALSE                       0
#endif



#ifdef __cplusplus
}
#endif



#endif  /* CONSTANT_H */
