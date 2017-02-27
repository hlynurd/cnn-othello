import ctypes
testlib = ctypes.CDLL('/home/hlynurd/Notebook/Othello/c_sandbox/zebra/zebralogic.so')
from numpy.ctypeslib import ndpointer
testlib.get_stability.restype = ndpointer(dtype=ctypes.c_int, shape=(100,))
testlib.get_mobility.restype = ndpointer(dtype=ctypes.c_int, shape=(100,))
BLACKSQ = 0
EMPTY = 1
WHITESQ = 2

pyarr = [EMPTY] * 100
pyarr[54] = BLACKSQ
pyarr[45] = BLACKSQ
pyarr[44] = WHITESQ
pyarr[55] = WHITESQ
arr = (ctypes.c_int * len(pyarr))(*pyarr)
stabs = testlib.get_stability(arr, BLACKSQ)
print(stabs)
mobs = testlib.get_mobility(arr, BLACKSQ)
