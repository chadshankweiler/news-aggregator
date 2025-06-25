from flask import Flask, jsonify, request
import glob, json, psycopg2, hashlib, re, html, subprocess, os, re
import psycopg2
from psycopg2.extras import execute_values

app = Flask(__name__)

@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})


@app.route('/news', methods=["POST"])
def add_guide():
    rows = []

    raw = request.get_json(force=True, silent=True)
    if not raw or "data" not in raw:
        return jsonify(error="JSON must contain 'name'"), 400

    json_raw = json.loads(raw["data"])

    articles = json_raw["articles"]

    for a in articles: 
        row = {
            "id" : a.get("id"),
            "county" : meta.get("county"),
            "state" : meta.get("state"),
            "country" : meta.get("country"),
            "title" : a.get("title"),
            "published_utc" : a.get("published_utc"),
            "source" : a.get("source"),
            "url" : a.get("url"),
            "summary" : a.get("summary"),
        }
        rows.append(row)

    print(rows)

    return jsonify(rows), 201   

@app.route('/huh', methods=["POST"])
def test():

    conn = psycopg2.connect("dbname=postgres user=postgres password=lol host=localhost port=5432")

    cur = conn.cursor()

    # regex to remove markdown from json data
    pattern = re.compile(r"```json\s*(\{[\s\S]*?\})\s*```", re.DOTALL)

    rows = []

    # raw data
    raw = request.get_json(force=True, silent=True)
    if not raw or "data" not in raw:
        return jsonify(error="JSON must contain 'name'"), 400

    markdown_block = raw["data"]

    # remove markdown from text
    match = pattern.search(markdown_block)

    # convert to json
    payload = json.loads(match.group(1))

    # append to rows array
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

    return jsonify(payload), 201   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
