#!/usr/bin/env python3
"""Generate profile SVGs (heatmap, stats, languages) from the GitHub GraphQL API.

Uses only the Python standard library. Run by .github/workflows/stats.yml every day.
Env:
  GH_LOGIN        GitHub username (default: tareq199923)
  GH_STATS_TOKEN  optional personal access token (read:user) to include private contributions
  GITHUB_TOKEN    fallback token provided by GitHub Actions
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from xml.sax.saxutils import escape

LOGIN = os.environ.get("GH_LOGIN", "tareq199923")
TOKEN = os.environ.get("GH_STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
EXCLUDE_LANGS = {"HTML", "CSS", "Jupyter Notebook", "TeX"}
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

BG, BORDER, TEXT, MUTED = "#0d1117", "#30363d", "#e6edf3", "#8b949e"
RAMP = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
FONT = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


PROFILE_Q = """
query($login:String!, $from:DateTime!, $to:DateTime!){
  user(login:$login){
    createdAt
    followers{ totalCount }
    contributionsCollection(from:$from, to:$to){
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount weekday } }
      }
    }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      nodes{
        stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){
          edges{ size node{ name color } }
        }
      }
    }
  }
}
"""

CAL_Q = """
query($login:String!, $from:DateTime!, $to:DateTime!){
  user(login:$login){
    contributionsCollection(from:$from, to:$to){
      contributionCalendar{ weeks{ contributionDays{ date contributionCount } } }
    }
  }
}
"""


def svg_wrap(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}">'
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="{BG}" stroke="{BORDER}"/>'
        f"{body}</svg>"
    )


def level(count, mx):
    if count <= 0:
        return 0
    r = count / mx
    return 1 if r <= 0.25 else 2 if r <= 0.5 else 3 if r <= 0.75 else 4


def heatmap_svg(weeks, total):
    cell, gap, left, top = 15, 3, 40, 50
    step = cell + gap
    w = left + len(weeks) * step + 20
    h = top + 7 * step + 50
    mx = max([d["contributionCount"] for wk in weeks for d in wk["contributionDays"]] + [1])
    b = [f'<text x="20" y="28" font-size="14" font-weight="600" fill="{TEXT}">Contributions</text>']
    b.append(
        f'<text x="{w-20}" y="28" font-size="12" text-anchor="end" fill="{MUTED}">'
        f"{total:,} in the last year</text>"
    )
    last_month = None
    for i, wk in enumerate(weeks):
        x = left + i * step
        first = wk["contributionDays"][0]["date"]
        month = datetime.strptime(first, "%Y-%m-%d").strftime("%b")
        if month != last_month:
            b.append(f'<text x="{x}" y="{top-8}" font-size="10" fill="{MUTED}">{month}</text>')
            last_month = month
        for d in wk["contributionDays"]:
            y = top + d["weekday"] * step
            c = d["contributionCount"]
            lv = level(c, mx)
            b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{RAMP[lv]}"/>')
            tcolor = TEXT if lv >= 1 else MUTED
            b.append(
                f'<text x="{x + cell/2}" y="{y + cell/2 + 2.6}" font-size="7" text-anchor="middle" '
                f'fill="{tcolor}">{c}</text>'
            )
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b.append(f'<text x="12" y="{top + row*step + 11}" font-size="10" fill="{MUTED}">{name}</text>')
    ly = top + 7 * step + 22
    lx = w - 20 - 5 * (cell + 4) - 70
    b.append(f'<text x="{lx}" y="{ly+11}" font-size="10" fill="{MUTED}">Less</text>')
    for i, col in enumerate(RAMP):
        b.append(f'<rect x="{lx + 28 + i*(cell+4)}" y="{ly}" width="{cell}" height="{cell}" rx="3" fill="{col}"/>')
    b.append(f'<text x="{lx + 28 + 5*(cell+4) + 2}" y="{ly+11}" font-size="10" fill="{MUTED}">More</text>')
    return svg_wrap(w, h, "".join(b))


def stats_svg(items):
    w, h = 860, 300
    b = [f'<text x="30" y="40" font-size="18" font-weight="600" fill="{TEXT}">GitHub stats</text>']
    cols, col_w = 3, (w - 60) // 3
    for i, (value, label) in enumerate(items):
        x = 30 + (i % cols) * col_w
        y = 100 + (i // cols) * 76
        b.append(f'<text x="{x}" y="{y}" font-size="28" font-weight="600" fill="{TEXT}">{escape(str(value))}</text>')
        b.append(f'<text x="{x}" y="{y+22}" font-size="13" fill="{MUTED}">{escape(label)}</text>')
    return svg_wrap(w, h, "".join(b))


def langs_svg(langs):
    w, h = 860, 200
    total = sum(s for _, s, _ in langs) or 1
    b = [f'<text x="30" y="40" font-size="18" font-weight="600" fill="{TEXT}">Top languages</text>']
    bar_x, bar_w = 30, w - 60
    b.append(f'<clipPath id="bar"><rect x="{bar_x}" y="58" width="{bar_w}" height="10" rx="5"/></clipPath>')
    x = bar_x
    segs = []
    for name, size, color in langs:
        sw = bar_w * size / total
        segs.append(f'<rect x="{x:.2f}" y="58" width="{sw:.2f}" height="10" fill="{color}"/>')
        x += sw
    b.append(f'<g clip-path="url(#bar)">{"".join(segs)}</g>')
    for i, (name, size, color) in enumerate(langs):
        lx = 30 + (i % 3) * ((w - 60) // 3)
        ly = 104 + (i // 3) * 34
        pct = 100 * size / total
        b.append(f'<circle cx="{lx+5}" cy="{ly-5}" r="5" fill="{color}"/>')
        b.append(
            f'<text x="{lx+18}" y="{ly}" font-size="13" fill="{TEXT}">{escape(name)} '
            f'<tspan fill="{MUTED}">{pct:.1f}%</tspan></text>'
        )
    return svg_wrap(w, h, "".join(b))


def streaks(days):
    counts = dict(days)
    dates = sorted(counts)
    longest = run = 0
    prev = None
    for d in dates:
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        if counts[d] > 0:
            run = run + 1 if prev and (dt - prev).days == 1 else 1
            longest = max(longest, run)
            prev = dt
        else:
            run, prev = 0, None
    today = datetime.now(timezone.utc).date()
    cur, day = 0, today
    if counts.get(day.isoformat(), 0) == 0:
        day -= timedelta(days=1)
    while counts.get(day.isoformat(), 0) > 0:
        cur += 1
        day -= timedelta(days=1)
    return cur, longest


def main():
    if not TOKEN:
        raise SystemExit("No token found. Set GITHUB_TOKEN or GH_STATS_TOKEN.")
    os.makedirs(OUT, exist_ok=True)
    now = datetime.now(timezone.utc)
    data = gql(PROFILE_Q, {"login": LOGIN, "from": iso(now - timedelta(days=365)), "to": iso(now)})["user"]
    cc = data["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    total = cc["contributionCalendar"]["totalContributions"]

    # all-time daily counts for streaks, one request per calendar year
    created = datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    days = {}
    for year in range(created.year, now.year + 1):
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), now)
        cal = gql(CAL_Q, {"login": LOGIN, "from": iso(start), "to": iso(end)})["user"]
        for wk in cal["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in wk["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
    cur, longest = streaks(days.items())

    repos = data["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    lang_sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n in EXCLUDE_LANGS:
                continue
            size, color = lang_sizes.get(n, (0, e["node"]["color"] or "#8b949e"))
            lang_sizes[n] = (size + e["size"], color)
    langs = sorted(((n, s, c) for n, (s, c) in lang_sizes.items()), key=lambda x: -x[1])[:6]

    items = [
        (f"{total:,}", "Contributions (last year)"),
        (f"{cc['totalCommitContributions']:,}", "Commits (last year)"),
        (f"{cc['totalPullRequestContributions']:,}", "Pull requests (last year)"),
        (f"{cc['totalIssueContributions']:,}", "Issues (last year)"),
        (f"{cc['totalRepositoriesWithContributedCommits']:,} repos", "Contributed to (last year)"),
        (f"{stars:,}", "Stars earned"),
        (f"{data['followers']['totalCount']:,}", "Followers"),
        (f"{cur} days", "Current streak"),
        (f"{longest} days", "Longest streak"),
    ]

    for name, content in (
        ("heatmap.svg", heatmap_svg(weeks, total)),
        ("stats.svg", stats_svg(items)),
        ("langs.svg", langs_svg(langs or [("No data yet", 1, "#8b949e")])),
    ):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
    print("Generated assets in", OUT)


if __name__ == "__main__":
    main()
