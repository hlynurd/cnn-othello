import numpy as np

def ffo_endgame_45():
    ffo_45 = np.zeros((8,8))
    ffo_45[5][0] = 1
    
    ffo_45[2][1] = 1
    ffo_45[3][1] = 1
    ffo_45[4][1] = 1
    ffo_45[5][1] = 1
    
    ffo_45[0][2] = -1
    ffo_45[1][2] = -1
    ffo_45[2][2] = 1
    ffo_45[3][2] = 1
    ffo_45[4][2] = 1
    ffo_45[5][2] = 1
    ffo_45[7][2] = -1
    
    ffo_45[0][3] = -1
    ffo_45[1][3] = -1
    ffo_45[2][3] = 1
    ffo_45[3][3] = -1
    ffo_45[4][3] = -1
    ffo_45[5][3] = 1
    ffo_45[6][3] = -1
    ffo_45[7][3] = -1
    
    ffo_45[0][4] = -1
    ffo_45[1][4] = -1
    ffo_45[2][4] = -1
    ffo_45[3][4] = -1
    ffo_45[4][4] = -1
    ffo_45[5][4] = -1
    ffo_45[6][4] = 1
    ffo_45[7][4] = -1
    
    ffo_45[0][5] = -1
    ffo_45[1][5] = -1
    ffo_45[2][5] = -1
    ffo_45[3][5] = -1
    ffo_45[4][5] = -1
    ffo_45[5][5] = 1
    ffo_45[6][5] = -1
    ffo_45[7][5] = -1
    
    ffo_45[0][6] = -1
    
    ffo_45[3][6] = -1
    ffo_45[4][6] = 1
    ffo_45[5][6] = 1
    
    ffo_45[7][6] = -1
    return ffo_45
    
def gen_pressibus_example():
    test = np.zeros((8,8))
    test[0][0] = 1
    test[3][0] = -1
    test[6][0] = -1
    test[1][0] = 1
    test[2][0] = 1
    test[4][0] = 1
    test[0][1] = 1
    test[1][1] = -1
    test[2][1] = 1
    test[3][1] = 1
    test[4][1] = -1
    test[5][1] = -1
    test[6][1] = -1
    test[7][1] = 1
    
    test[0][2] = -1
    test[1][2] = 1
    test[2][2] = 1
    test[3][2] = 1
    test[4][2] = -1
    test[5][2] = -1
    test[6][2] = 1
    test[7][2] = -1
    
    test[7][0] = 1

    test[1][2] = 1
    test[2][1] = 1
    test[2][2] = 1
    test[3][2] = 1

    test[6][2] = 1

    test[0][3] = 1
    test[4][3] = 1
    test[5][3] = -1
    test[6][3] = 1
    test[7][3] = 1
    
    test[3][4] = 1
    test[4][4] = -1
    test[6][4] = -1
    
    test[3][5] = -1
    test[6][5] = 1
    
    test[2][6] = 1
    test[4][6] = 1
    test[5][6] = 1
    test[6][6] = 1
    test[7][6] = 1
    
    test[1][7] = 1
    test[3][7] = 1
    test[4][7] = 1
    test[5][7] = 1
    test[6][7] = 1
    test[7][7] = 1
    return test

def gen_pressibus_example_c():
    BLACKSQ = 0
    EMPTY = 1
    WHITESQ = 2
    test = np.ones((8,8))
    test[0][0] = WHITESQ
    test[3][0] = BLACKSQ
    test[6][0] = BLACKSQ
    test[1][0] = WHITESQ
    test[2][0] = WHITESQ
    test[4][0] = WHITESQ
    test[0][1] = WHITESQ
    test[1][1] = BLACKSQ
    test[2][1] = WHITESQ
    test[3][1] = WHITESQ
    test[4][1] = BLACKSQ
    test[5][1] = BLACKSQ
    test[6][1] = BLACKSQ
    test[7][1] = WHITESQ
   
    test[0][2] = BLACKSQ
    test[1][2] = WHITESQ
    test[2][2] = WHITESQ
    test[3][2] = WHITESQ
    test[4][2] = BLACKSQ
    test[5][2] = BLACKSQ
    test[6][2] = WHITESQ
    test[7][2] = BLACKSQ
    
    test[7][0] = WHITESQ

    test[1][2] = WHITESQ
    test[2][1] = WHITESQ
    test[2][2] = WHITESQ
    test[3][2] = WHITESQ

    test[6][2] = WHITESQ

    test[0][3] = WHITESQ
    test[4][3] = WHITESQ
    test[5][3] = BLACKSQ
    test[6][3] = WHITESQ
    test[7][3] = WHITESQ
    
    test[3][4] = WHITESQ
    test[4][4] = BLACKSQ
    test[6][4] = BLACKSQ
    
    test[3][5] = BLACKSQ
    test[6][5] = WHITESQ
    
    test[2][6] = WHITESQ
    test[4][6] = WHITESQ
    test[5][6] = WHITESQ
    test[6][6] = WHITESQ
    test[7][6] = WHITESQ
    
    test[1][7] = WHITESQ
    test[3][7] = WHITESQ
    test[4][7] = WHITESQ
    test[5][7] = WHITESQ
    test[6][7] = WHITESQ
    test[7][7] = WHITESQ
    return test