import math

def add_patch():
    def log100(x):
        return math.log(x)/math.log(100)
    math.log100 = log100

add_patch()
print(math.log100(10))

import numpy as np 
def add_patch():
    def pii():
        return np.pi
    np.pii = pii

add_patch()
print(np.pii())
