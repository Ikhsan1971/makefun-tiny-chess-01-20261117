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
(150,000 nodes per move, iterative deepening, an unbounded-memory-safe
transposition-table cap) replaces any clock, so a
replayed trial makes identical moves. No network beyond the env, no
model calls, Python standard library only.

`main.py` is a `makefun compress` LZMA pack of its readable source
(`engine_src.py`, not in this snapshot for the 8 KB cap; the pair is
recorded in `~/.makefun/compress.json` and the source is sent beside the
transcripts as `packs/`). The pack was made by the kit's `node
cli/makefun.mjs compress`; the source byte-matches
(sha256 5969d45cb881a86397f0c8e8a650e990005bd11a7c833c0c84f018bff3ec4cb9)
and the packed program was run and verified locally (game 1 of practice
trial-0: win by checkmate, ~1.6 s per move).

## Run

    MAKEFUN_ENV_URL=http://... python3 main.py

It plays every game through the env (`/game`, `/move`) until the env
answers `done`. If a computed move is ever missing from the env's
`legal_moves`, it falls back to the best capture the env lists.

## Limits, honest score status

- Small alpha-beta engine: no tablebase, no book, no explicit
  king-safety term; expected to beat the weaker anchors and to lose to
  the nodes-500k-and-above anchors.
- The 430,000-node round exceeded the 1,800 s trial wall (≈5 s per move) and
  scored 0 because every unplayed game was lost; the current entry cuts the
  budget to 150,000 nodes (~1.7 s per move) and passes the first practice
  game. Practice Elo pending the platform's grade at submission.

## Files

- `main.py` — the packed engine (4,054 bytes, the whole engine).
- `LICENSE` — MIT; `README.md` — this file; `.makefun/owner.json` — claim.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
