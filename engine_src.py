# tiny-chess-01: compact chess engine (MIT, see LICENSE). This file is the
# readable source of main.py (packed with `makefun compress`, byte for byte).
# Plays every game via the env at MAKEFUN_ENV_URL. Stdlib only, fixed node
# budget (never a clock), no model calls.
import json, os, sys, urllib.request
ENV = os.environ.get("MAKEFUN_ENV_URL")
def post(p, b):
    if not ENV:
        sys.exit("MAKEFUN_ENV_URL is not set")
    r = urllib.request.Request(ENV + p, data=json.dumps(b).encode(), headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x:
            return json.load(x)
    except urllib.error.HTTPError as e:
        sys.exit(f"{p}: HTTP {e.code} {e.read().decode(errors='replace')}")
V = [0, 100, 320, 330, 500, 900, 0]
KN = (-33, -31, -18, -14, 14, 18, 31, 33)
KG = (-17, -16, -15, -1, 1, 15, 16, 17)
BD = (-17, -15, 15, 17)
RD = (-16, -1, 1, 16)
QD = BD + RD
PT = 'pnbrqk'
PS = [  # rank 8 first, white POV
[0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,30,30,30,40,40,30,30,30,20,20,20,35,35,20,20,20,15,15,15,25,25,15,15,15,10,10,10,20,20,10,10,10,5,5,5,0,0,5,5,5,0,0,0,0,0,0,0,0],
[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-30,-30,-30,-30,-30,-40,-50],
[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,5,10,10,10,10,5,-10,-10,0,10,10,10,10,0,-10,-20,-10,-10,-10,-10,-10,-10,-20],
[0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,10,10,5,0,-5,0,0,5,10,10,5,0,-5,-10,5,5,5,5,5,5,-10,-10,0,5,0,0,0,5,-10,-20,-40,-20,0,0,-20,-40,-20],
[-30,-20,-10,0,0,-10,-20,-30,-20,-10,0,0,0,0,-10,-20,-10,0,0,0,0,0,0,-10,0,0,0,10,10,0,0,0,0,10,10,10,10,10,10,0,-10,10,10,10,10,10,10,-10,-20,0,10,0,0,10,0,-20,-30,-20,-10,0,0,-10,-20,-30]]
def load(f):
    p = f.split()
    b = [0] * 128
    r, x = 7, 0
    for c in p[0]:
        if c == "/":
            r -= 1; x = 0
        elif c.isdigit():
            x += int(c)
        else:
            v = PT.index(c.lower()) + 1
            b[r * 16 + x] = v if c.isupper() else v + 8
            x += 1
    side = 1 if p[1] == "w" else -1
    cast = 0
    for c in p[2]:
        cast |= {"K": 1, "Q": 2, "k": 4, "q": 8}.get(c, 0)
    ep = -1
    if p[3] != "-":
        ep = (int(p[3][1]) - 1) * 16 + "abcdefgh".index(p[3][0])
    half = int(p[4]) if len(p) > 4 else 0
    return [b, side, cast, ep, half, b.index(6), b.index(14)]
def uc(m):
    f, t, pr = m & 127, (m >> 7) & 127, m >> 14
    return "abcdefgh"[f & 7] + str((f >> 4) + 1) + "abcdefgh"[t & 7] + str((t >> 4) + 1) + (PT[pr - 1] if pr else "")
def du(u):
    f = (int(u[1]) - 1) * 16 + "abcdefgh".index(u[0])
    t = (int(u[3]) - 1) * 16 + "abcdefgh".index(u[2])
    pr = PT.index(u[4]) + 1 if len(u) > 4 else 0
    return f | (t << 7) | (pr << 14)
def att(b, sq, by):
    o = 0 if by == 1 else 8
    d = 16 if by == 1 else -16
    for df in (-1, 1):
        s = sq - d + df
        if 0 <= s < 128 and not (s & 0x88) and b[s] == 1 + o:
            return True
    for q in KN:
        s = sq + q
        if 0 <= s < 128 and not (s & 0x88) and b[s] == 2 + o:
            return True
    for q in KG:
        s = sq + q
        if 0 <= s < 128 and not (s & 0x88) and b[s] == 6 + o:
            return True
    for rays, tl in ((BD, 3), (RD, 4)):
        for q in rays:
            s = sq + q
            while 0 <= s < 128 and not (s & 0x88):
                pc = b[s]
                if pc:
                    if pc == tl + o or pc == 5 + o:
                        return True
                    break
                s += q
    return False
def gen(b, side, cast, ep):
    out = []
    w = side == 1
    o = 0 if w else 8
    for sq in range(128):
        if sq & 0x88:
            continue
        pc = b[sq]
        if not pc or (pc < 8) != w:
            continue
        t = pc - o
        if t == 1:
            d = 16 if w else -16
            to = sq + d
            if not (to & 0x88) and b[to] == 0:
                if (to >> 4) == (7 if w else 0):
                    out += [sq | (to << 7) | (pr << 14) for pr in (5, 4, 3, 2)]
                else:
                    out.append(sq | (to << 7))
                    t2 = sq + 2 * d
                    if (sq >> 4) == (1 if w else 6) and b[t2] == 0:
                        out.append(sq | (t2 << 7))
            for df in (-1, 1):
                to = sq + d + df
                if to & 0x88:
                    continue
                cap = b[to]
                if (cap and (cap < 8) != w) or to == ep:
                    if (to >> 4) == (7 if w else 0):
                        out += [sq | (to << 7) | (pr << 14) for pr in (5, 4, 3, 2)]
                    else:
                        out.append(sq | (to << 7))
        elif t == 6:
            for q in KG:
                to = sq + q
                if not (to & 0x88):
                    cap = b[to]
                    if not cap or (cap < 8) != w:
                        out.append(sq | (to << 7))
            if sq == (4 if w else 116):
                if w:
                    if cast & 1 and b[5] == 0 and b[6] == 0 and not (att(b, 4, -1) or att(b, 5, -1) or att(b, 6, -1)):
                        out.append(4 | (6 << 7))
                    if cast & 2 and b[3] == 0 and b[2] == 0 and b[1] == 0 and not (att(b, 4, -1) or att(b, 3, -1) or att(b, 2, -1)):
                        out.append(4 | (2 << 7))
                else:
                    if cast & 4 and b[117] == 0 and b[118] == 0 and not (att(b, 116, 1) or att(b, 117, 1) or att(b, 118, 1)):
                        out.append(116 | (118 << 7))
                    if cast & 8 and b[115] == 0 and b[114] == 0 and b[113] == 0 and not (att(b, 116, 1) or att(b, 115, 1) or att(b, 114, 1)):
                        out.append(116 | (114 << 7))
        elif t == 2:
            for q in KN:
                to = sq + q
                if 0 <= to < 128 and not (to & 0x88):
                    cap = b[to]
                    if not cap or (cap < 8) != w:
                        out.append(sq | (to << 7))
        else:
            for q in (BD if t == 3 else RD if t == 4 else QD):
                to = sq + q
                while 0 <= to < 128 and not (to & 0x88):
                    cap = b[to]
                    if cap:
                        if (cap < 8) != w:
                            out.append(sq | (to << 7))
                        break
                    out.append(sq | (to << 7))
                    to += q
    return out
def mk(st, m):
    b, side, cast, ep, half = st[:5]
    f, t, pr = m & 127, (m >> 7) & 127, m >> 14
    pc = b[f]
    tt = pc if pc < 8 else pc - 8
    cap = b[t]
    cs = -1
    if tt == 1 and t == ep and cap == 0 and (f & 7) != (t & 7):
        cs = t - (16 if side == 1 else -16)
        cap = b[cs]
    undo = (cap, cast, ep, half, cs, pc, st[5 if side == 1 else 6])
    b[t] = (pr if side == 1 else pr + 8) if pr else pc
    b[f] = 0
    if cs >= 0:
        b[cs] = 0
    c = cast
    if tt == 6:
        c &= ~3 if side == 1 else ~12
        if side == 1:
            st[5] = t
        else:
            st[6] = t
    if f == 0 or t == 0: c &= ~2
    if f == 7 or t == 7: c &= ~1
    if f == 112 or t == 112: c &= ~8
    if f == 119 or t == 119: c &= ~4
    if tt == 6 and abs(t - f) == 2:
        if t == 6:   b[5], b[7] = b[7], 0
        elif t == 2: b[3], b[0] = b[0], 0
        elif t == 118: b[117], b[119] = b[119], 0
        elif t == 114: b[115], b[112] = b[112], 0
    nep = -1
    if tt == 1 and abs(t - f) == 32:
        nep = (f + t) // 2
    half = 0 if (tt == 1 or cap) else half + 1
    st[1] = -side; st[2] = c; st[3] = nep; st[4] = half
    return undo
def um(st, m, undo):
    b, side, cast, ep, half = st[:5]
    side = -side
    cap, cast0, ep0, half0, cs, pc, ksq0 = undo
    f, t, pr = m & 127, (m >> 7) & 127, m >> 14
    tt = pc if pc < 8 else pc - 8
    if tt == 6 and abs(t - f) == 2:
        if t == 6:   b[7], b[5] = b[5], 0
        elif t == 2: b[0], b[3] = b[3], 0
        elif t == 118: b[119], b[117] = b[117], 0
        elif t == 114: b[112], b[115] = b[115], 0
    if tt == 6:
        if side == 1:
            st[5] = ksq0
        else:
            st[6] = ksq0
    b[f] = pc
    b[t] = 0
    if cs >= 0:
        b[cs] = cap
    else:
        b[t] = cap
    st[1] = side; st[2] = cast0; st[3] = ep0; st[4] = half0
def ev(b):
    s = bw = bb = 0
    for sq in range(128):
        if sq & 0x88:
            continue
        pc = b[sq]
        if not pc:
            continue
        if pc < 8:
            t = pc
            s += V[t] + PS[t - 1][(7 - (sq >> 4)) * 8 + (sq & 7)]
            if t == 3: bw += 1
        else:
            t = pc - 8
            s -= V[t] + PS[t - 1][(sq >> 4) * 8 + (sq & 7)]
            if t == 3: bb += 1
    if bw >= 2: s += 30
    if bb >= 2: s -= 30
    return s
N = [0]
LIM = 150000
PATH = []
GAME = []
TT = {}
def sk(st):
    return bytes(st[0]) + bytes((st[1] + 1, st[2], st[3] + 1))
def mvv(st, m, ply, kill):
    b = st[0]
    f, t, pr = m & 127, (m >> 7) & 127, m >> 14
    s = 900000 if pr else 0
    cap = b[t]
    if not cap and (b[f] if b[f] < 8 else b[f] - 8) == 1 and (f & 7) != (t & 7):
        cap = 1 if st[1] == -1 else 9
    if cap:
        s += 500000 + 10 * V[cap if cap < 8 else cap - 8] - V[b[f] if b[f] < 8 else b[f] - 8]
    elif m in kill[ply]:
        s += 100000
    return s
def qs(st, m):
    b = st[0]
    f, t, pr = m & 127, (m >> 7) & 127, m >> 14
    s = 900000 if pr else 0
    cap = b[t]
    if not cap and (b[f] if b[f] < 8 else b[f] - 8) == 1 and (f & 7) != (t & 7):
        cap = 1 if st[1] == -1 else 9
    if cap:
        s += 10 * V[cap if cap < 8 else cap - 8] - V[b[f] if b[f] < 8 else b[f] - 8]
    return s
def qsearch(st, a, b, ply):
    N[0] += 1
    if N[0] > LIM:
        raise StopIteration
    side = st[1]
    s = ev(st[0])
    if side == -1:
        s = -s
    if s >= b:
        return b
    if s > a:
        a = s
    bd = st[0]
    ms = [m for m in gen(bd, side, st[2], st[3]) if qs(st, m) > 0]
    ms.sort(key=lambda m: -qs(st, m))
    for m in ms:
        un = mk(st, m)
        ks = st[5 if side == 1 else 6]
        if att(bd, ks, -side):
            um(st, m, un)
            continue
        v = -qsearch(st, -b, -a, ply + 1)
        um(st, m, un)
        if v >= b:
            return b
        if v > a:
            a = v
    return a
def ab(st, d, a, b, ply, kill):
    if N[0] > LIM:
        raise StopIteration
    N[0] += 1
    sd = st[1]
    if st[4] >= 100:
        return 0
    k = sk(st)
    te = TT.get(k)
    if te is not None and te[0] >= d:
        if te[1] == 0 or (te[1] == 1 and te[2] >= b) or (te[1] == 2 and te[2] <= a):
            return te[2]
    if k in GAME or k in PATH:
        return 0
    incheck = att(st[0], st[5 if sd == 1 else 6], -sd)
    if d <= 0:
        if incheck:
            d = 1
        else:
            return qsearch(st, a, b, ply)
    ms = gen(st[0], sd, st[2], st[3])
    ms.sort(key=lambda m: -mvv(st, m, ply, kill))
    PATH.append(k)
    best = -100001
    cnt = 0
    for m in ms:
        un = mk(st, m)
        ks = st[5 if sd == 1 else 6]
        if att(st[0], ks, -sd):
            um(st, m, un)
            continue
        cnt += 1
        v = -ab(st, d - 1, -b, -a, ply + 1, kill)
        um(st, m, un)
        if v > best:
            best = v
        if v > a:
            a = v
        if a >= b:
            ks2 = kill[ply]
            if m not in ks2:
                ks2.append(m)
                if len(ks2) > 2:
                    ks2.pop(0)
            break
    PATH.pop()
    r = best if cnt else (-100000 + ply if incheck else 0)
    if len(TT) < 300000:
        TT[k] = (d, 0 if (a < r < b) else (1 if r >= b else 2), r)
    return r
def root(st, hist):
    global GAME
    GAME = hist
    N[0] = 0
    sd = st[1]
    ms = gen(st[0], sd, st[2], st[3])
    kill = [[] for _ in range(128)]
    ms.sort(key=lambda m: -mvv(st, m, 0, kill))
    ok = []
    for m in ms:
        un = mk(st, m)
        ks = st[5 if sd == 1 else 6]
        if not att(st[0], ks, -sd):
            ok.append(m)
        um(st, m, un)
    if not ok:
        return None
    if len(TT) > 120000:
        TT.clear()
    best = ok[0]
    for d in range(1, 64):
        a = -100001
        cb = None
        cv = -100001
        try:
            for m in ([best] + [m for m in ok if m != best]):
                un = mk(st, m)
                v = -ab(st, d - 1, -100000, -a, 1, kill)
                um(st, m, un)
                if cb is None or v > cv:
                    cv = v; cb = m
                if v > a:
                    a = v
        except StopIteration:
            break
        if cb is not None:
            best = cb
        if cv > 90000:
            break
    return best
START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
def hist_keys(mv):
    st = load(START)
    keys = [sk(st)]
    for u in mv:
        mk(st, du(u))
        keys.append(sk(st))
    return keys
def fb(g):
    vals = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}
    board = {}
    for i, row in enumerate(g["fen"].split()[0].split("/")):
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            else:
                board["abcdefgh"[f] + str(8 - i)] = c.lower()
                f += 1
    def rank(e):
        v = board.get(e[2:4])
        if v is None and board.get(e[:2]) == "p" and e[0] != e[2]:
            v = "p"
        return (-(vals[v] if v else 0), e)
    return min(g["legal_moves"], key=rank)
def main():
    while True:
        g = post("/game", {})
        if g["status"] == "done":
            break
        while g["status"] == "your_move":
            st = load(g["fen"])
            m = root(st, hist_keys(g["moves"]))
            u = uc(m) if m is not None else None
            if u not in g.get("legal_moves", []):
                u = fb(g)
                print("fallback move used", file=sys.stderr)
            g = post("/move", {"game": g["game"], "move": u})
        print(f"game {g['game']}: {g.get('outcome')} by {g.get('reason')}", file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
if __name__ == "__main__":
    main()
