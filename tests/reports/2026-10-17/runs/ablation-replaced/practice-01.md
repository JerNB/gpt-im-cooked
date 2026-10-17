# Practice 01

Original synthetic practice. Basis: [course-packet.md](course-packet.md), S4.

`tickets` has three rows, with `wait_min` values `4`, `NA`, and `8`. You run `tickets |> summarize(avg_wait = mean(wait_min, na.rm = TRUE))` without assigning anything back to `tickets`.

What value is returned for `avg_wait`, and how many rows remain in the original `tickets`? Explain in one sentence.

Write your attempt before opening [the separate solution](practice-01-solution.md).
