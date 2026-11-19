# makefun-tiny-chess-01-20261117

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Ikhsan1971/makefun-tiny-chess-01-20261117/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Ikhsan1971/makefun-tiny-chess-01-20261117/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A compact chess engine for the make.fun `tiny-chess-01` competition,
shipped as one `main.py` of ≤ 4,096 bytes.

Idea: full legal move generation (castling, en passant, promotion,
checks) and a negamax alpha-beta search with quiescence search,
MVV-LVA ordering and an iterative-deepening root, plus one-ply check
extension. Evaluation is material + piece-square tables for
pawn/knight/king (mirrored for black) + the bishop pair; 50-move and
repetition inside the search score 0. A fixed node budget
(130,000 nodes per move, a capped transposition table) replaces any
clock, so a replayed trial makes identical moves. No network beyond
the env, no model calls, Python standard library only. This engine
was authored fresh for this entry (64-square signed board, own move
encoding and eval tables); it is not derived from any earlier build.

`main.py` is a `makefun compress` LZMA pack of its readable source
(`engine_src.py`, not in this snapshot for the 8 KB cap; the pair is
recorded in `~/.makefun/compress.json` and the source is sent beside the
transcripts as `packs/`). The pack was made by the kit's `node
cli/makefun.mjs compress`; the source byte-matches
(sha256 2c0fb9e9ef4727c487ad969b6654874be21487ab594b181042383f358843ff26).

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
  scored 0 because every unplayed game was lost; this build runs at
  130,000 nodes per move.
- Authentic practice trial-0 (seed 33447412) completed all 6 games with no
  crashes and no fallback moves after the king-attack fix: 1 win by
  checkmate (vs the depth-2 anchor), 5 losses by checkmate (vs depth-3/4
  and nodes-100k/250k/500k). Practice Elo pending the platform's grade at
  submission.

## Files

- `main.py` — the packed engine (3,571 bytes, the whole engine).
- `LICENSE` — MIT; `README.md` — this file; `.makefun/owner.json` — claim.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
