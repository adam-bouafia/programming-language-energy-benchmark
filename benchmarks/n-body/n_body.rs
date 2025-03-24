// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// n-body benchmark in Rust

use std::env;
use std::f64::consts::PI;

const SOLAR_MASS: f64 = 4.0 * PI * PI;
const DAYS_PER_YEAR: f64 = 365.24;

struct Body {
    x: f64, y: f64, z: f64,
    vx: f64, vy: f64, vz: f64,
    mass: f64,
}

impl Body {
    fn new(x: f64, y: f64, z: f64, vx: f64, vy: f64, vz: f64, mass: f64) -> Body {
        Body { x, y, z, vx, vy, vz, mass }
    }

    fn jupiter() -> Body {
        Body::new(
            4.84143144246472090e+00,
            -1.16032004402742839e+00,
            -1.03622044471123109e-01,
            1.66007664274403694e-03 * DAYS_PER_YEAR,
            7.69901118419740425e-03 * DAYS_PER_YEAR,
            -6.90460016972063023e-05 * DAYS_PER_YEAR,
            9.54791938424326609e-04 * SOLAR_MASS,
        )
    }

    fn saturn() -> Body {
        Body::new(
            8.34336671824457987e+00,
            4.12479856412430479e+00,
            -4.03523417114321381e-01,
            -2.76742510726862411e-03 * DAYS_PER_YEAR,
            4.99852801234917238e-03 * DAYS_PER_YEAR,
            2.30417297573763929e-05 * DAYS_PER_YEAR,
            2.85885980666130812e-04 * SOLAR_MASS,
        )
    }

    fn uranus() -> Body {
        Body::new(
            1.28943695621391310e+01,
            -1.51111514016986312e+01,
            -2.23307578892655734e-01,
            2.96460137564761618e-03 * DAYS_PER_YEAR,
            2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR,
            4.36624404335156298e-05 * SOLAR_MASS,
        )
    }

    fn neptune() -> Body {
        Body::new(
            1.53796971148509165e+01,
            -2.59193146099879641e+01,
            1.79258772950371181e-01,
            2.68067772490389322e-03 * DAYS_PER_YEAR,
            1.62824170038242295e-03 * DAYS_PER_YEAR,
            -9.51592254519715870e-05 * DAYS_PER_YEAR,
            5.15138902046611451e-05 * SOLAR_MASS,
        )
    }

    fn sun() -> Body {
        Body::new(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS)
    }
}

fn offset_momentum(bodies: &mut [Body]) {
    let mut px = 0.0;
    let mut py = 0.0;
    let mut pz = 0.0;

    for body in bodies.iter() {
        px += body.vx * body.mass;
        py += body.vy * body.mass;
        pz += body.vz * body.mass;
    }

    bodies[0].vx = -px / SOLAR_MASS;
    bodies[0].vy = -py / SOLAR_MASS;
    bodies[0].vz = -pz / SOLAR_MASS;
}

fn advance(bodies: &mut [Body], dt: f64) {
    let nbodies = bodies.len();

    for i in 0..nbodies {
        for j in i+1..nbodies {
            let dx = bodies[i].x - bodies[j].x;
            let dy = bodies[i].y - bodies[j].y;
            let dz = bodies[i].z - bodies[j].z;

            let dsq = dx * dx + dy * dy + dz * dz;
            let distance = dsq.sqrt();
            let mag = dt / (dsq * distance);

            bodies[i].vx -= dx * bodies[j].mass * mag;
            bodies[i].vy -= dy * bodies[j].mass * mag;
            bodies[i].vz -= dz * bodies[j].mass * mag;

            bodies[j].vx += dx * bodies[i].mass * mag;
            bodies[j].vy += dy * bodies[i].mass * mag;
            bodies[j].vz += dz * bodies[i].mass * mag;
        }
    }

    for body in bodies.iter_mut() {
        body.x += dt * body.vx;
        body.y += dt * body.vy;
        body.z += dt * body.vz;
    }
}

fn energy(bodies: &[Body]) -> f64 {
    let mut e = 0.0;
    let nbodies = bodies.len();

    for i in 0..nbodies {
        e += 0.5 * bodies[i].mass * (
            bodies[i].vx * bodies[i].vx +
            bodies[i].vy * bodies[i].vy +
            bodies[i].vz * bodies[i].vz
        );

        for j in i+1..nbodies {
            let dx = bodies[i].x - bodies[j].x;
            let dy = bodies[i].y - bodies[j].y;
            let dz = bodies[i].z - bodies[j].z;

            let distance = (dx * dx + dy * dy + dz * dz).sqrt();
            e -= (bodies[i].mass * bodies[j].mass) / distance;
        }
    }
    e
}

fn main() {
    let n = env::args()
        .nth(1)
        .and_then(|n| n.parse().ok())
        .unwrap_or(1000);

    let mut bodies = [
        Body::sun(),
        Body::jupiter(),
        Body::saturn(),
        Body::uranus(),
        Body::neptune(),
    ];

    offset_momentum(&mut bodies);
    println!("{:.9}", energy(&bodies));

    for _ in 0..n {
        advance(&mut bodies, 0.01);
    }

    println!("{:.9}", energy(&bodies));
}
