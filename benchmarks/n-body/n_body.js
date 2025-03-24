/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * n-body benchmark in JavaScript
 */

'use strict';

const PI = 3.141592653589793;
const SOLAR_MASS = 4 * PI * PI;
const DAYS_PER_YEAR = 365.24;

class Body {
  constructor(x, y, z, vx, vy, vz, mass) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.vx = vx;
    this.vy = vy;
    this.vz = vz;
    this.mass = mass;
  }

  static jupiter() {
    return new Body(
      4.84143144246472090e+00,
      -1.16032004402742839e+00,
      -1.03622044471123109e-01,
      1.66007664274403694e-03 * DAYS_PER_YEAR,
      7.69901118419740425e-03 * DAYS_PER_YEAR,
      -6.90460016972063023e-05 * DAYS_PER_YEAR,
      9.54791938424326609e-04 * SOLAR_MASS
    );
  }

  static saturn() {
    return new Body(
      8.34336671824457987e+00,
      4.12479856412430479e+00,
      -4.03523417114321381e-01,
      -2.76742510726862411e-03 * DAYS_PER_YEAR,
      4.99852801234917238e-03 * DAYS_PER_YEAR,
      2.30417297573763929e-05 * DAYS_PER_YEAR,
      2.85885980666130812e-04 * SOLAR_MASS
    );
  }

  static uranus() {
    return new Body(
      1.28943695621391310e+01,
      -1.51111514016986312e+01,
      -2.23307578892655734e-01,
      2.96460137564761618e-03 * DAYS_PER_YEAR,
      2.37847173959480950e-03 * DAYS_PER_YEAR,
      -2.96589568540237556e-05 * DAYS_PER_YEAR,
      4.36624404335156298e-05 * SOLAR_MASS
    );
  }

  static neptune() {
    return new Body(
      1.53796971148509165e+01,
      -2.59193146099879641e+01,
      1.79258772950371181e-01,
      2.68067772490389322e-03 * DAYS_PER_YEAR,
      1.62824170038242295e-03 * DAYS_PER_YEAR,
      -9.51592254519715870e-05 * DAYS_PER_YEAR,
      5.15138902046611451e-05 * SOLAR_MASS
    );
  }

  static sun() {
    return new Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS);
  }
}

function offsetMomentum(bodies) {
  let px = 0, py = 0, pz = 0;
  
  for (const body of bodies) {
    px += body.vx * body.mass;
    py += body.vy * body.mass;
    pz += body.vz * body.mass;
  }
  
  bodies[0].vx = -px / SOLAR_MASS;
  bodies[0].vy = -py / SOLAR_MASS;
  bodies[0].vz = -pz / SOLAR_MASS;
}

function advance(bodies, dt) {
  for (let i = 0; i < bodies.length; ++i) {
    const iBody = bodies[i];
    
    for (let j = i + 1; j < bodies.length; ++j) {
      const jBody = bodies[j];
      const dx = iBody.x - jBody.x;
      const dy = iBody.y - jBody.y;
      const dz = iBody.z - jBody.z;
      
      const dSquared = dx * dx + dy * dy + dz * dz;
      const distance = Math.sqrt(dSquared);
      const mag = dt / (dSquared * distance);
      
      iBody.vx -= dx * jBody.mass * mag;
      iBody.vy -= dy * jBody.mass * mag;
      iBody.vz -= dz * jBody.mass * mag;
      
      jBody.vx += dx * iBody.mass * mag;
      jBody.vy += dy * iBody.mass * mag;
      jBody.vz += dz * iBody.mass * mag;
    }
  }
  
  for (const body of bodies) {
    body.x += dt * body.vx;
    body.y += dt * body.vy;
    body.z += dt * body.vz;
  }
}

function energy(bodies) {
  let e = 0;
  
  for (let i = 0; i < bodies.length; ++i) {
    const iBody = bodies[i];
    e += 0.5 * iBody.mass * (iBody.vx * iBody.vx + iBody.vy * iBody.vy + iBody.vz * iBody.vz);
    
    for (let j = i + 1; j < bodies.length; ++j) {
      const jBody = bodies[j];
      const dx = iBody.x - jBody.x;
      const dy = iBody.y - jBody.y;
      const dz = iBody.z - jBody.z;
      
      const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
      e -= (iBody.mass * jBody.mass) / distance;
    }
  }
  
  return e;
}

function main() {
  const n = process.argv.length > 2 ? parseInt(process.argv[2]) : 1000;
  
  const bodies = [
    Body.sun(),
    Body.jupiter(),
    Body.saturn(),
    Body.uranus(),
    Body.neptune()
  ];
  
  offsetMomentum(bodies);
  console.log(energy(bodies).toFixed(9));
  
  for (let i = 0; i < n; ++i) {
    advance(bodies, 0.01);
  }
  
  console.log(energy(bodies).toFixed(9));
}

main();
