import numpy as np

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