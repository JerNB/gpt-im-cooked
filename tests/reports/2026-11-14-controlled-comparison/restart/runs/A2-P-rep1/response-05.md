I’ll record Q4 as correct and distinguish what you’ve demonstrated from what still needs checking.

**Q4 is correct: 2 element-to-element comparisons**, comparing `0` with `-1`, then `-1` with `3`.

Your Q3 and Q4 answers show progress with **counting adjacent-pair comparisons**. We haven’t yet checked broader loop tracing: recording the current index, values read, and each state change in execution order, as Notes §2.1 requires. So I wouldn’t call loop tracing mastered yet.

Quick check: **If a loop changes a list value, when should you record that change in your trace?**

Progress saved.