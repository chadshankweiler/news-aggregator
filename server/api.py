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
    pattern = re.compile(r"```json\s*(\{[\s\S]*?\})\s*```", re.DOTALL)

    rows = []

    raw = request.get_json(force=True, silent=True)
    if not raw or "data" not in raw:
        return jsonify(error="JSON must contain 'name'"), 400

    markdown_block = raw["data"]

    match = pattern.search(markdown_block)

    payload = json.loads(match.group(1))

    articles = payload["articles"]

    for a in articles: 
        row = {
            "id" : a.get("id"),
            "title" : a.get("title"),
            "published_utc" : a.get("published_utc"),
            "source" : a.get("source"),
            "url" : a.get("url"),
            "summary" : a.get("summary"),
        }
        rows.append(row)

    print(rows)

    return jsonify(payload), 201   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
