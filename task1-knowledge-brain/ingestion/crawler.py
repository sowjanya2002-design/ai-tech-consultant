"""Async sitemap crawler with checkpointing, retries and change detection."""
import asyncio, hashlib, json, os, re, sqlite3
import httpx
from bs4 import BeautifulSoup

SITEMAP = "https://support.brilliantdirectories.com/support/sitemap.xml"
DB = os.path.join(os.path.dirname(__file__), "..", "kb.sqlite")


def db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS pages(url TEXT PRIMARY KEY, title TEXT, text TEXT,
        images TEXT, hash TEXT, status TEXT, attempts INT DEFAULT 0)""")
    con.execute("CREATE TABLE IF NOT EXISTS escalations(id INTEGER PRIMARY KEY, question TEXT, answer TEXT)")
    return con


async def get_article_urls(client):
    xml = (await client.get(SITEMAP)).text
    return [u for u in re.findall(r"<loc>(.*?)</loc>", xml) if "/articles/" in u]


def parse(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else url
    body = soup.find("article") or soup.body
    images = [i["src"] for i in body.find_all("img") if i.get("src", "").startswith("http")][:5]
    text = " ".join(body.get_text(" ").split())
    return title, text, images


async def fetch_one(client, sem, con, url):
    async with sem:
        for attempt in range(3):
            try:
                r = await client.get(url, timeout=30)
                r.raise_for_status()
                title, text, images = parse(r.text, url)
                h = hashlib.sha256(text.encode()).hexdigest()
                old = con.execute("SELECT hash FROM pages WHERE url=?", (url,)).fetchone()
                status = "unchanged" if old and old[0] == h else "changed"
                con.execute("INSERT OR REPLACE INTO pages VALUES(?,?,?,?,?,?,?)",
                            (url, title, text, json.dumps(images), h, status, attempt + 1))
                con.commit()
                return status
            except Exception:
                await asyncio.sleep(2 ** attempt)
        con.execute("INSERT OR REPLACE INTO pages(url,status,attempts) VALUES(?,?,3)", (url, "failed"))
        con.commit()
        return "failed"


async def crawl(limit=int(os.getenv("MAX_ARTICLES", "300"))):
    con = db()
    async with httpx.AsyncClient(follow_redirects=True, headers={"User-Agent": "KnowledgeBrain/1.0"}) as client:
        urls = (await get_article_urls(client))[:limit]
        sem = asyncio.Semaphore(5)
        results = await asyncio.gather(*(fetch_one(client, sem, con, u) for u in urls))
    summary = {s: results.count(s) for s in set(results)}
    print("crawl summary:", summary)
    return summary


if __name__ == "__main__":
    asyncio.run(crawl())
