import math

x = -1

def abs(x):
    if x >= 0:
        return x
    n = math.sqrt(x ** 2)
    return abs(type(x)(n))

print(abs(x))


