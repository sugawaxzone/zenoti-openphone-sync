from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENPHONE_API_KEY = os.getenv("OPENPHONE_API_KEY")

def create_openphone_contact(first_name, last_name, phone, email):
    url = "https://api.openphone.co/v1/contacts"
    headers = {
        "Authorization": f"Bearer {OPENPHONE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "properties": {
            "firstName": first_name,
            "lastName": last_name,
            "phoneNumbers": [phone],
            "emails": [email]
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route("/zenoti-webhook", methods=["POST"])
def zenoti_webhook():
    data = request.json
    first_name = data.get("FirstName", "Guest")
    last_name = data.get("LastName", "")
    phone = data.get("Phone", "")
    email = data.get("Email", "")

    if phone:
        result = create_openphone_contact(first_name, last_name, phone, email)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Missing phone number"}), 400

app.run(host='0.0.0.0', port=3000)
