# List aliasing application: separate key

- Item ID: P1-alias-copy-1
- Original synthetic practice; scope basis: materials/notes.md sections 1.1-1.3.
- Question: x = [3, 8]; y = x; z = x.copy(); y[0] = 6. Give final x, y, z and explain their object relationships.
- Answer: x and y are [6, 8]; z is [3, 8]. Assignment makes x and y refer to the same list. The shallow copy creates a separate outer list for z, so replacing an element of y changes the shared x/y list only.
- Answer evidence: Verified computation with local Python assertions; reasoning supported by Notes sections 1.1-1.3.
- Target: Initial application after an explained example; no student response reviewed yet. Does not by itself establish transfer.
