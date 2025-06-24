from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})


@app.route('/news', methods=["POST"])
def add_guide():
    payload = request.get_json(force=True, silent=True)
    if not payload or "name" not in payload:
        return jsonify(error="JSON must contain 'name'"), 400

    # Normally you’d write to a database; here we echo back a stub record
    new_item = {
        "id": 1,            # replace with real ID from your DB
        "name": payload["name"],
        "details": payload.get("details", "")
    }
    return jsonify(new_item), 201   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
