from flask import Flask, jsonify, request
import glob, json, psycopg2, hashlib, re, html, subprocess, os, re
import psycopg2
from psycopg2.extras import execute_values


conn = psycopg2.connect("dbname=postgres user=postgres password=lol host=localhost port=5432")

cur = conn.cursor()

rows = []

JSON_BLOCK = re.compile(r"```json\s*(\{[\s\S]*?\})\s*```", re.DOTALL)

test = {'data': '```json\n{\n  "query": {\n    "county": "Miami-Dade County",\n    "state": "Florida",\n    "country": "United States",\n    "date_from": "2025-06-24T17:23:00Z",\n    "date_to": "2025-06-25T17:23:00Z",\n    "generated_utc": "2025-06-25T17:23:00Z"\n  },\n  "articles": [\n    {\n      "id": "3f2e5b8d6c9a4d1e2b7c8f0a9d4e1b2c3a4d5e6f",\n      "title": "Woman appeals dismissal of Miami‑Dade schools sexual abuse lawsuit",\n      "published_utc": "2025-06-25T14:17:00Z",\n      "source": "CBS Miami",\n      "url": "https://www.cbsnews.com/miami/news/woman-appeals-dismissal-of-miami-dade-schools-sexual-abuse-lawsuit/",\n      "summary": "A woman who alleges sexual abuse by a middle school teacher has appealed the dismissal of her lawsuit against the Miami‑Dade School Board on statute‑of‑limitations grounds."\n    },\n    {\n      "id": "4a1b2c3d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",\n      "title": "Police investigation shuts down stretch of Palmetto Expressway",\n      "published_utc": "2025-06-25T15:00:00Z",\n      "source": "NBC Miami",\n      "url": "https://www.nbcmiami.com/news/local/police-investigation-shuts-down-stretch-of-palmetto-expressway/3644879/",\n      "summary": "A section of the Palmetto Expressway in Miami‑Dade was closed Tuesday night as police conducted an ongoing investigation."\n    },\n    {\n      "id": "5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c",\n      "title": "2 children ejected from vehicle after Turnpike crash in southwest Miami‑Dade",\n      "published_utc": "2025-06-25T15:48:00Z",\n      "source": "WPLG Local\u202f10",\n      "url": "https://www.local10.com/news/local/2025/06/25/2-children-ejected-from-vehicle-after-turnpike-crash-in-southwest-miami-dade/",\n      "summary": "Two children were ejected from a Honda following a two‑vehicle collision on the Turnpike in southwest Miami‑Dade; both sustained non‑life‑threatening injuries."\n    },\n    {\n      "id": "6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d",\n      "title": "Miami‑Dade man attacked victim with garden stone after refusing kiss, deputies say",\n      "published_utc": "2025-06-25T15:34:00Z",\n      "source": "WPLG Local\u202f10",\n      "url": "https://www.local10.com/news/local/2025/06/25/miami-dade-man-attacked-victim-with-garden-stone-after-refusing-kiss-deputies-say/",\n      "summary": "A 23‑year‑old man allegedly assaulted another with a garden stone after a sexual advance was rejected, causing facial injuries, say deputies."\n    }\n  ]\n}\n```'}

huh = test["data"]

m = JSON_BLOCK.search(huh)

payload = json.loads(m.group(1))

print(payload)

meta = payload["query"]
for article in payload["articles"]:
    sha = article["id"] or canonical_sha(article["title"], article["summary"])
    rows.append((
        sha,
        meta["county"],
        meta["state"],
        meta["country"],
        article["title"],
        article["published_utc"],
        article["source"],
        article["url"],
        article.get("summary"),
        json.dumps(article, ensure_ascii=False)
    ))

insert_sql = """
    INSERT INTO news_articles
      (id, county, state, country, title, published_utc,
       source, url, summary, raw)
    VALUES %s
    ON CONFLICT (id) DO NOTHING;
"""

execute_values(cur, insert_sql, rows, page_size=500)
conn.commit()

cur.execute("SELECT COUNT(*) FROM news_articles;")
print(cur.fetchone()[0], "rows now in table")


cur.close()
conn.close()

