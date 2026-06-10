from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Sample email list with duplicates
email_list = [
    "john@example.com",
    "alice@example.com",
    "bob@example.com",
    "john@example.com",
    "alice@example.com"
]

email_set = set(email_list)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Email Duplicate Checker API is running",
        "usage": "POST /check-email with JSON { 'email': 'example@mail.com' }"
    })

@app.route("/check-email", methods=["POST"])
def check_email():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error": "Send JSON with 'email' field"}), 400

    email = data["email"].strip().lower()

    start = time.time()
    exists_in_list = email in email_list
    list_time = (time.time() - start) * 1_000_000  # microseconds

    start = time.time()
    exists_in_set = email in email_set
    set_time = (time.time() - start) * 1_000_000  # microseconds

    return jsonify({
        "email": email,
        "exists_in_list": exists_in_list,
        "exists_in_set": exists_in_set,
        "list_time_microseconds": list_time,
        "set_time_microseconds": set_time,
        "explanation": "List lookup is O(n). Set lookup is O(1). Sets are faster for membership checks."
    })

if __name__ == "__main__":
    app.run(debug=True)
