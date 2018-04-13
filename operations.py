import math
def length(u): 
    return (u[0]**2 + u[1]**2)**0.5

def angle(u, v):
    scalar = u[0] * v[0] + u[1] * v[1]
    L = length(u) * length(v)
    return 0 if L ==0 else math.acos(scalar / L)

def dist(p1, p2):
    return ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )**0.5

def add(p1, p2):
    return ( p1[0]+p2[0], p1[1]+p2[1] )

def sub(p1, p2):
    return ( p1[0]-p2[0], p1[1]-p2[1] )