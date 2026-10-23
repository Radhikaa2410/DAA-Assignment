#!/usr/bin/env python3
"""Live ASCII 0/1 knapsack DP visualizer.
Usage: python3 knapsack_live.py data.txt [--test K] [--delay 0.15] [--plain]
  --plain : no ANSI redraw; print snapshots (useful for logs / copy-paste)
Legend: [x] = cell being computed, <x> = "skip item" source, (x) = "take item" source
"""
import sys, time, argparse
from knapsack import parse

CLR = "\033[H\033[J"
def render(n, W, items, dp, cur, src_skip, src_take, msg, ansi, chosen=()):
    cw = 5
    out = [msg, ""]
    out.append(" " * 20 + "".join(f"{w:>{cw}}" for w in range(W + 1)))
    for i in range(n + 1):
        label = "i=0 (no items)" if i == 0 else f"i={i} w={items[i-1][0]},v={items[i-1][1]}"
        row = f"{label:<20}"
        for w in range(W + 1):
            v = dp[i][w]
            s = "." if v is None else str(v)
            if (i, w) == cur:
                cell = f"[{s}]"
                cell = f"\033[1;43;30m{cell:>{cw}}\033[0m" if ansi else f"{cell:>{cw}}"
            elif (i, w) == src_skip:
                cell = f"<{s}>"
                cell = f"\033[36m{cell:>{cw}}\033[0m" if ansi else f"{cell:>{cw}}"
            elif (i, w) == src_take:
                cell = f"({s})"
                cell = f"\033[32m{cell:>{cw}}\033[0m" if ansi else f"{cell:>{cw}}"
            elif (i, w) in chosen:
                cell = f"\033[1;35m{s:>{cw}}\033[0m" if ansi else f"{s+'*':>{cw}}"
            else:
                cell = f"{s:>{cw}}"
            row += cell
        out.append(row)
    return "\n".join(out)

def run(n, W, items, delay, ansi):
    dp = [[None] * (W + 1) for _ in range(n + 1)]
    for w in range(W + 1): dp[0][w] = 0
    def show(cur=None, sk=None, tk=None, msg="", chosen=(), pause=delay):
        if ansi: print(CLR, end="")
        else: print()
        print(render(n, W, items, dp, cur, sk, tk, msg, ansi, chosen), flush=True)
        time.sleep(pause)
    show(msg=f"Init: row 0 = 0   (n={n}, W={W})")
    for i in range(1, n + 1):
        wt, val = items[i - 1]
        for w in range(W + 1):
            skip = dp[i - 1][w]
            if wt <= w:
                take = dp[i - 1][w - wt] + val
                dp[i][w] = max(skip, take)
                msg = (f"dp[{i}][{w}] = max(skip {skip}, take {dp[i-1][w-wt]}+{val}={take}) = {dp[i][w]}")
                show((i, w), (i - 1, w), (i - 1, w - wt), msg)
            else:
                dp[i][w] = skip
                msg = f"dp[{i}][{w}]: item weight {wt} > {w}, copy {skip}"
                show((i, w), (i - 1, w), None, msg)
    # backtrack
    chosen, w, picked = set(), W, []
    for i in range(n, 0, -1):
        chosen.add((i, w))
        if dp[i][w] != dp[i - 1][w]:
            picked.append(i); w -= items[i - 1][0]
    chosen.add((0, w))
    show(msg=f"DONE. Max value = {dp[n][W]}   items chosen: {sorted(picked)}   (path marked)", chosen=chosen, pause=0)
    return dp[n][W]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--test", type=int, default=0)
    ap.add_argument("--delay", type=float, default=0.15); ap.add_argument("--plain", action="store_true")
    a = ap.parse_args()
    cases = parse(a.file)
    sel = [a.test - 1] if a.test else range(len(cases))
    for k in sel:
        n, W, items = cases[k]
        print(f"\n######## Test {k+1} ########")
        run(n, W, items, a.delay, ansi=not a.plain and sys.stdout.isatty())
        if len(sel) > 1: time.sleep(1.5)