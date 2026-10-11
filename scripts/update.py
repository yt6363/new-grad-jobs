"""Rewrite README.md from Find your role first's public entry-level list. Standard library only."""
import json
import urllib.request
from datetime import datetime, timezone

SOURCE = "https://findyourrolefirst.click/api/public/entry-level"
ORDER = ["product", "data", "design", "business", "software"]


def age(stamp, now):
    try:
        then = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return ""
    hours = max(0, int((now - then).total_seconds() // 3600))
    return f"{hours}h" if hours < 48 else f"{hours // 24}d"


def cell(text):
    return str(text or "").replace("|", "/").replace("\n", " ").strip()


def main():
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "new-grad-jobs-readme (github.com/yt6363/new-grad-jobs)"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    now = datetime.now(timezone.utc)
    tracks = data["tracks"]
    total = sum(len(tracks[k]["jobs"]) for k in ORDER if k in tracks)
    lines = [
        "# New grad and entry-level jobs (US)",
        "",
        "New grad and entry-level roles in **product, data, design, business and software**, posted in the last 7 days, "
        "read straight from more than 15,000 company career sites (Greenhouse, Lever, Ashby, Workday and the big tech "
        "career sites). **Updated every hour.**",
        "",
        f"Last update: {now.strftime('%B %d, %Y, %H:%M UTC')} · {total} roles listed",
        "",
        "Want these the hour they're posted, for your role and city? [Find your role first](https://findyourrolefirst.click) "
        "searches every new role as it appears, free for your first 200 roles, and works inside Claude and Codex.",
        "",
        "## Jump to",
        "",
    ]
    for key in ORDER:
        if key in tracks:
            label = tracks[key]["label"]
            lines.append(f"- [{label}](#{label.lower().replace(',', '').replace(' ', '-')}) ({len(tracks[key]['jobs'])})")
    for key in ORDER:
        if key not in tracks:
            continue
        track = tracks[key]
        lines += ["", f"## {track['label']}", "", "| Company | Role | Location | Posted | Apply |", "|---|---|---|---|---|"]
        for job in track["jobs"]:
            company = cell(job["company"])
            if job.get("company_page"):
                company = f"[{company}]({job['company_page']})"
            lines.append(f"| {company} | {cell(job['title'])} | {cell(job['location'])[:60]} | {age(job.get('posted'), now)} | "
                         f"[Open]({job['url']}) |")
        if not track["jobs"]:
            lines.append("| | Nothing new this week | | | |")
    lines += ["", "---", "",
              "Roles come from each company's own careers site, newest first. Titles, companies and places only; "
              "open a role to see the posting and apply on the company's site. Spot a mistake? Open an issue.",
              "", "More: [who's hiring this week](https://findyourrolefirst.click/blog/hiring) · "
              "[startups that just raised and are hiring](https://findyourrolefirst.click/raises) · "
              "[hiring trends by company](https://findyourrolefirst.click/companies)", ""]
    with open("README.md", "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


if __name__ == "__main__":
    main()
