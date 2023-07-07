use num::integer::gcd;
use rayon::prelude::*;
use std::env;

fn coprime(a: i32, b: i32) -> bool {
    gcd(a, b) == 1
}

fn is_jstrict(n: i32, a: i32, b: i32) -> bool {
    if b == 1 {
        return a == 1 || coprime(a, b);
    }

    if a < b {
        return is_jstrict(n, b, a);
    }

    if !(coprime(a, b) && coprime(a, n) && coprime(b, n)) {
        return false;
    }

    if n == a + b {
        return true;
    }

    if n < a + b {
        return false;
    }

    if a > 1 && !is_jstrict(a, (-n).rem_euclid(a), b) {
        return false;
    }

    if b > 1 && !is_jstrict(b, a.rem_euclid(b), (-n).rem_euclid(b)) {
        return false;
    }

    true
}

#[test]
fn is_jstrict_tests() {
    for (n, a, b) in [(5, 3, 2), (7, 4, 3), (21, 8, 13), (11, 2, 3)] {
        assert!(is_jstrict(n, a, b), "{}, ({}, {}) not JStrict", n, a, b);
    }

    for (n, a, b) in [(5, 4, 3)] {
        assert!(!is_jstrict(n, a, b), "{}, ({}, {}) not JStrict", n, a, b);
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    assert_eq!(args.len(), 3, "usage: {} LOWER UPPER", args[0]);
    let l = args[1].parse::<i32>().unwrap();
    let u = args[2].parse::<i32>().unwrap();

    (l..u).into_par_iter().for_each(|n| {
        for a in 3..n {
            for b in 2..a {
                if is_jstrict(n, a, b) {
                    assert!(!is_jstrict(a, n.rem_euclid(a), b));
                    assert!(!is_jstrict(n, n - a, b));
                    let mut found = false;
                    let mut x = n;
                    while x > 0 && !found {
                        x -= a;
                        if x % b == 0 {
                            found = true;
                        }
                    }
                    if !found {
                        println!("{} {} {}", n, a, b);
                    }

                }
            }
        }
    });
    println!("Success!")
}
