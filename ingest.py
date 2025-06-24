import glob, json, psycopg2, hashlib, re, html
import psycopg2
from psycopg2.extras import execute_values



def canonical_sha(title, body):
    print("asdf")

conn = psycopg2.connect("dbname=postgres user=postgres password=lol host=localhost port=5432")

cur = conn.cursor()

check = glob.glob('news/**/*.txt', recursive=True, include_hidden=True)


rows = []

doc = json.load(open(check[3]))
meta = doc["query"]
for article in doc["articles"]:
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
