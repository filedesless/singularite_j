coprime a b = gcd a b == 1

pairwise f xs = [f x y | (i, x) <- zip [0 ..] xs, (j, y) <- zip [1 .. i] xs]

coprime2 = and . pairwise coprime

smooth (_ : t) = all (<= 1) t

blowup (h : t) =
  [ x : [if i /= j then y `mod` x else (-h) `mod` x | (j, y) <- zip [1 ..] t]
    | (i, x) <- zip [1 ..] t,
      x > 1
  ]

isJStrict xs = smooth xs || coprime2 xs && all isJStrict (blowup xs)

group n = filter (coprime n) [1 .. n]

phi = length . group

isNice n = 3 * (phi n - 1) == length (filter isJStrict [[n, a, b] | a <- group n, b <- group n])

main = do
  print [i | i <- [1 .. 200], isNice i]