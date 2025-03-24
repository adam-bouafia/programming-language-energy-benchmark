#!/usr/bin/env python3
"""
The Computer Language Benchmarks Game
https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

n-body benchmark in Python
"""

import sys
from math import sqrt

def advance(bodies, dt, n):
    for i in range(n):
        for (x1, y1, z1, vx1, vy1, vz1, m1), (x2, y2, z2, vx2, vy2, vz2, m2) in pairs(bodies):
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            
            mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            
            b1_vx = vx1 - dx * m2 * mag
            b1_vy = vy1 - dy * m2 * mag
            b1_vz = vz1 - dz * m2 * mag
            
            b2_vx = vx2 + dx * m1 * mag
            b2_vy = vy2 + dy * m1 * mag
            b2_vz = vz2 + dz * m1 * mag
            
            bodies[i] = (x1, y1, z1, b1_vx, b1_vy, b1_vz, m1)
            bodies[i+1] = (x2, y2, z2, b2_vx, b2_vy, b2_vz, m2)
        
        for i, (x, y, z, vx, vy, vz, m) in enumerate(bodies):
            bodies[i] = (x + dt * vx, y + dt * vy, z + dt * vz, vx, vy, vz, m)

def energy(bodies):
    e = 0.0
    
    for i, (x1, y1, z1, vx1, vy1, vz1, m1) in enumerate(bodies):
        e += 0.5 * m1 * (vx1 * vx1 + vy1 * vy1 + vz1 * vz1)
        
        for x2, y2, z2, vx2, vy2, vz2, m2 in bodies[i+1:]:
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            e -= (m1 * m2) / sqrt(dx * dx + dy * dy + dz * dz)
    
    return e

def offset_momentum(bodies):
    px = py = pz = 0.0
    
    for x, y, z, vx, vy, vz, m in bodies:
        px += vx * m
        py += vy * m
        pz += vz * m
    
    bodies[0] = (bodies[0][0], bodies[0][1], bodies[0][2], 
                -px / SOLAR_MASS, -py / SOLAR_MASS, -pz / SOLAR_MASS, 
                bodies[0][6])

def pairs(bodies):
    result = []
    for i in range(0, len(bodies)-1, 2):
        result.append((bodies[i], bodies[i+1]))
    return result

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES = [
    # Sun
    (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS),
    
    # Jupiter
    (4.84143144246472090e+00,
     -1.16032004402742839e+00,
     -1.03622044471123109e-01,
     1.66007664274403694e-03 * DAYS_PER_YEAR,
     7.69901118419740425e-03 * DAYS_PER_YEAR,
     -6.90460016972063023e-05 * DAYS_PER_YEAR,
     9.54791938424326609e-04 * SOLAR_MASS),
    
    # Saturn
    (8.34336671824457987e+00,
     4.12479856412430479e+00,
     -4.03523417114321381e-01,
     -2.76742510726862411e-03 * DAYS_PER_YEAR,
     4.99852801234917238e-03 * DAYS_PER_YEAR,
     2.30417297573763929e-05 * DAYS_PER_YEAR,
     2.85885980666130812e-04 * SOLAR_MASS),
    
    # Uranus
    (1.28943695621391310e+01,
     -1.51111514016986312e+01,
     -2.23307578892655734e-01,
     2.96460137564761618e-03 * DAYS_PER_YEAR,
     2.37847173959480950e-03 * DAYS_PER_YEAR,
     -2.96589568540237556e-05 * DAYS_PER_YEAR,
     4.36624404335156298e-05 * SOLAR_MASS),
    
    # Neptune
    (1.53796971148509165e+01,
     -2.59193146099879641e+01,
     1.79258772950371181e-01,
     2.68067772490389322e-03 * DAYS_PER_YEAR,
     1.62824170038242295e-03 * DAYS_PER_YEAR,
     -9.51592254519715870e-05 * DAYS_PER_YEAR,
     5.15138902046611451e-05 * SOLAR_MASS)
]

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    bodies = BODIES.copy()
    
    offset_momentum(bodies)
    print(f"{energy(bodies):.9f}")
    
    for i in range(n):
        advance(bodies, 0.01, len(bodies)//2)
    
    print(f"{energy(bodies):.9f}")

if __name__ == "__main__":
    main()
