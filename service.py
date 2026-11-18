"""Customer accounts REST API."""
import os
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_talisman import Talisman

_ACCOUNTS = {}


def create_app(test_config=None):
    """Application factory."""
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-only"),
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    origins = [
        item.strip()
        for item in os.environ.get("CORS_ORIGINS", "").split(",")
        if item.strip()
    ]
    CORS(app, resources={r"/*": {"origins": origins}} if origins else {},
         supports_credentials=False)
    Talisman(
        app,
        force_https=not app.config.get("TESTING", False),
        content_security_policy={
            "default-src": ["'self'"],
            "object-src": ["'none'"],
            "frame-ancestors": ["'none'"],
        },
    )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.post("/accounts")
    def create_account():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400
        name = payload.get("name")
        email = payload.get("email")
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "name is required"}), 400
        if not isinstance(email, str) or "@" not in email:
            return jsonify({"error": "a valid email is required"}), 400
        if any(row["email"].lower() == email.strip().lower()
               for row in _ACCOUNTS.values()):
            return jsonify({"error": "email already exists"}), 409
        account_id = str(uuid4())
        account = {
            "id": account_id,
            "name": name.strip(),
            "email": email.strip().lower(),
            "status": payload.get("status", "active"),
        }
        _ACCOUNTS[account_id] = account
        return jsonify(account), 201

    @app.get("/accounts")
    def list_accounts():
        return jsonify(list(_ACCOUNTS.values())), 200

    @app.get("/accounts/<account_id>")
    def read_account(account_id):
        account = _ACCOUNTS.get(account_id)
        if account is None:
            return jsonify({"error": "account not found"}), 404
        return jsonify(account), 200

    @app.put("/accounts/<account_id>")
    def update_account(account_id):
        account = _ACCOUNTS.get(account_id)
        if account is None:
            return jsonify({"error": "account not found"}), 404
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400
        updated = dict(account)
        if "name" in payload:
            if not isinstance(payload["name"], str) or not payload["name"].strip():
                return jsonify({"error": "name must be a non-empty string"}), 400
            updated["name"] = payload["name"].strip()
        if "email" in payload:
            email = payload["email"]
            if not isinstance(email, str) or "@" not in email:
                return jsonify({"error": "a valid email is required"}), 400
            normalized = email.strip().lower()
            if any(
                key != account_id and row["email"].lower() == normalized
                for key, row in _ACCOUNTS.items()
            ):
                return jsonify({"error": "email already exists"}), 409
            updated["email"] = normalized
        if "status" in payload:
            if payload["status"] not in ("active", "inactive"):
                return jsonify({"error": "status must be active or inactive"}), 400
            updated["status"] = payload["status"]
        _ACCOUNTS[account_id] = updated
        return jsonify(updated), 200

    @app.delete("/accounts/<account_id>")
    def delete_account(account_id):
        if account_id not in _ACCOUNTS:
            return jsonify({"error": "account not found"}), 404
        del _ACCOUNTS[account_id]
        return "", 204

    return app


app = create_app()
