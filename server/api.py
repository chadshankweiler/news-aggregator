from flask import Flask, jsonify, request
import glob, json, psycopg2, hashlib, re, html, subprocess, os, re
import psycopg2
from psycopg2.extras import execute_values

app = Flask(__name__)

def extract_location(text):
    # Use NLP model to extract locations (spaCy or OpenAI)
    return "South Beach"  

def geocode_location(place_name):
    # Geocode to lat/lng (geopy/Nominatim or Google)
    return 25.7826, -80.1341  

def categorize_article(title, summary):
    # Use simple rule-based or LLM-driven categorization
    return "Crime"  # placeholder

def is_actionable(article):
    # NLP to determine if actionable event (crime, hazards, emergency)
    return True  

def extract_claims(text):
    # LLM or regex-based claim extraction
    return ["Suspect arrested", "Road blocked due to accident"]  


@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})



@app.route('/news', methods=["POST"])
def test():

    conn = psycopg2.connect("dbname=news_geo user=postgres password=lol host=localhost port=5432")

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

        # Placeholder for NLP & geocoding:
        location_name = extract_location(article["summary"] or article["title"])
        latitude, longitude = geocode_location(location_name) if location_name else (None, None)

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
            json.dumps(article, ensure_ascii=False),
            location_name,
            f'POINT({longitude} {latitude})' if latitude and longitude else None,
            categorize_article(article["title"], article.get("summary")),
            is_actionable(article),
            extract_claims(article.get("summary", ""))
        ))


    insert_sql = """
        INSERT INTO news_articles
      (id, county, state, country, title, published_utc, source, url,
       summary, raw, location_name, geom, category, actionable, extracted_claims)
    VALUES %s
    ON CONFLICT (id) DO NOTHING;
    """

    execute_values(cur, insert_sql, rows, template="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s,4326),%s,%s,%s)", page_size=500)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM news_articles;")
    print(cur.fetchone()[0], "rows now in table")


    cur.close()
    conn.close()

    return jsonify(payload), 201   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
