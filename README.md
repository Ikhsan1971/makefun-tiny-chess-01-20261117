# makefun-tiny-chess-01-20261117

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Ikhsan1971/makefun-tiny-chess-01-20261117/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Ikhsan1971/makefun-tiny-chess-01-20261117/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A compact chess engine for the make.fun `tiny-chess-01` competition,
shipped as one `main.py` of ≤ 4,096 bytes.

Idea: full legal move generation (castling, en passant, promotion,
checks) and a negamax alpha-beta search with quiescence, MVV-LVA and
killer-move ordering, plus one-ply check extension. Evaluation is
material + piece-square tables (mirrored for black) + the bishop pair;
50-move and repetition inside the search score 0. A fixed node budget
(110,000 nodes per move, iterative deepening) replaces any clock, so a
replayed trial makes identical moves. No network beyond the env, no
model calls, Python standard library only.

`main.py` is a `makefun compress` LZMA pack of its readable source
(`engine_src.py`, not in this snapshot for the 8 KB cap; the pair is
recorded in `~/.makefun/compress.json` and the source is sent beside the
transcripts as `packs/`). The pack was made by the kit's `node
cli/makefun.mjs compress`; the source byte-matches
(sha256 c68461750e7191466581b3a9d9eb17f8923c94537ff841907304b9de83aea1eb)
and the packed program was run and verified locally.

## Run

    MAKEFUN_ENV_URL=http://... python3 main.py

It plays every game through the env (`/game`, `/move`) until the env
answers `done`. If a computed move is ever missing from the env's
`legal_moves`, it falls back to the best capture the env lists.

## Limits, honest score status

- Small alpha-beta engine: no tablebase, no book, no explicit
  king-safety term; expected to beat the weaker anchors and to lose to
  the nodes-500k-and-above anchors.
- Not graded yet: no practice Elo is claimed. Development machine had
  no Docker, so the dev trial was validated only against a fake env
  (legality, determinism, crash-freedom), not via `grade-local`.

## Files

- `main.py` — the packed engine (3,945 bytes, the whole engine).
- `LICENSE` — MIT; `README.md` — this file; `.makefun/owner.json` — claim.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
