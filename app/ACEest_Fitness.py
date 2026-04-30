"""ACEest Fitness Flask application."""

from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def create_app() -> Flask:
    """Application factory for easier testing and deployment."""
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    members: list[dict[str, Any]] = [
        {"id": 1, "name": "Aarav Sharma", "membership": "active", "plan_id": "basic"},
        {"id": 2, "name": "Diya Patel", "membership": "active", "plan_id": "pro"},
        {"id": 3, "name": "Rohan Mehta", "membership": "paused", "plan_id": "elite"},
    ]

    plans: list[dict[str, Any]] = [
        {"id": "basic", "name": "Basic Plan", "price_inr": 1499, "duration_months": 1},
        {"id": "pro", "name": "Pro Plan", "price_inr": 3999, "duration_months": 3},
        {"id": "elite", "name": "Elite Plan", "price_inr": 7499, "duration_months": 6},
    ]

    @app.get("/health")
    def health() -> tuple[Any, int]:
        return jsonify({"status": "OK"}), 200

    @app.get("/members")
    def get_members() -> tuple[Any, int]:
        return jsonify({"count": len(members), "members": members}), 200

    @app.get("/plans")
    def get_plans() -> tuple[Any, int]:
        return jsonify({"count": len(plans), "plans": plans}), 200

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> tuple[Any, int]:
        response = {
            "error": {
                "code": error.code,
                "name": error.name,
                "message": error.description,
            }
        }
        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(_: Exception) -> tuple[Any, int]:
        # Keep responses safe in production by avoiding internal error leakage.
        return jsonify({"error": {"code": 500, "name": "Internal Server Error"}}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
