import sys, re

def parse(path):
    cases, cur = [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line.startswith("#Test"):
            cur = []; cases.append(cur)
        elif line and cur is not None:
            cur.append(tuple(map(int, line.split())))
    return [(c[0][0], c[0][1], c[1:]) for c in cases]

def knapsack(n, W, items, show=False):
    dp = [[0]*(W+1) for _ in range(n+1)]
    if show:
        print(f"\nCapacity columns: 0..{W}")
        print("     w=  " + " ".join(f"{w:3d}" for w in range(W+1)))
        print("i=0 (none) " + " ".join(f"{0:3d}" for _ in range(W+1)))
    for i in range(1, n+1):
        wt, val = items[i-1]
        for w in range(W+1):
            dp[i][w] = dp[i-1][w]
            if wt <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-wt] + val)
        if show:
            row = " ".join(f"{x:3d}" for x in dp[i])
            print(f"i={i} (w={wt},v={val}) ".ljust(11) + row)
    return dp[n][W]

if __name__ == "__main__":
    path = sys.argv[1]
    out = []
    for t, (n, W, items) in enumerate(parse(path), 1):
        print(f"\n===== Test {t}: n={n}, W={W} =====")
        r = knapsack(n, W, items, show=True)
        print(f"-> Max value: {r}")
        out.append(f"#Test{t} {n} {W}  {r}")
    open("result.txt", "w").write("\n".join(out) + "\n")
    print("\n" + "\n".join(out))