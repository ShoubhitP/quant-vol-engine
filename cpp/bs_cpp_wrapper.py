import ctypes
import os

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), 'libbs.dylib')
lib = ctypes.CDLL(lib_path)

# Set argument and return types
lib.bs_call.restype = ctypes.c_double
lib.bs_call.argtypes = [ctypes.c_double] * 5

lib.bs_put.restype = ctypes.c_double
lib.bs_put.argtypes = [ctypes.c_double] * 5

def bs_call(S, K, vol, r, T):
    return lib.bs_call(S, K, vol, r, T)

def bs_put(S, K, vol, r, T):
    return lib.bs_put(S, K, vol, r, T)