import os
import sys
import pathlib
import datetime
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

# ── Make sure our internal packages resolve ────────────────────────────────────
# Adds the project root to PYTHONPATH so `src.*` imports work everywhere
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.routes.user   import user_bp
# (add other blueprints when they’re ready)
# from src.routes.orders import orders_bp
# from src.routes.projects import projects_bp
# …

# ── Flask app & config ─────────────────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)
app.config["SECRET_KEY"] = "handleserv#2024$secure"

# CORS: allow any origin (tighten later if you like)
CORS(app, origins="*")

app.register_blueprint(user_bp, url_prefix="/api")
# app.register_blueprint(orders_bp,   url_prefix="/api")
# app.register_blueprint(projects_bp, url_prefix="/api")

# ── Database (SQLite for demo) ─────────────────────────────────────────────────
BASE_DIR = pathlib.Path(__file__).resolve().parent          # /opt/render/project/src
DB_DIR   = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)                                 # make .../database if missing
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_DIR / 'app.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# ── API routes ────────────────────────────────────────────────────────────────
# Video Consultation
@app.post("/api/consultation/request")
def consultation_request():
    data = request.get_json(force=True)

    required = ["name", "email", "projectType", "description"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"{', '.join(missing)} required"}), 400

    consultation_id = f"CONS_{datetime.datetime.now():%Y%m%d_%H%M%S}"
    consultation    = {
        "id": consultation_id,
        "name": data["name"],
        "email": data["email"],
        "phone": data.get("phone", ""),
        "projectType": data["projectType"],
        "budget": data.get("budget", "$100"),
        "timeline": data.get("timeline", ""),
        "description": data["description"],
        "preferredTime": data.get("preferredTime", ""),
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat(),
        "price": "$100",
    }

    return jsonify(
        {
            "success": True,
            "message": "Consultation request received successfully!",
            "consultationId": consultation_id,
            "data": consultation,
        }
    ), 200


# Developers list
@app.get("/api/consultation/developers")
def get_developers():
    developers = [
        {
            "id": 1,
            "name": "Sarah Johnson",
            "specialty": "Business Websites & E-commerce",
            "experience": "5+ years",
            "rating": 4.9,
            "projects": 150,
            "price": "$100",
            "available": True,
        },
        {
            "id": 2,
            "name": "Mike Chen",
            "specialty": "Custom Web Applications",
            "experience": "7+ years",
            "rating": 4.8,
            "projects": 200,
            "price": "$100",
            "available": True,
        },
        {
            "id": 3,
            "name": "Lisa Rodriguez",
            "specialty": "UI/UX Design & Development",
            "experience": "6+ years",
            "rating": 4.9,
            "projects": 180,
            "price": "$100",
            "available": True,
        },
    ]
    return jsonify({"developers": developers}), 200


# Contact form
@app.post("/api/contact")
def contact_form():
    data = request.get_json(force=True)

    required = ["name", "email", "subject", "message"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"{', '.join(missing)} required"}), 400

    message_id = f"MSG_{datetime.datetime.now():%Y%m%d_%H%M%S}"
    # In production, save to DB here
    return (
        jsonify(
            {
                "success": True,
                "message": "Message sent successfully! We will get back to you within 24 hours.",
                "messageId": message_id,
            }
        ),
        200,
    )


# Portfolio
@app.get("/api/portfolio")
def get_portfolio():
    portfolio_items = [
        {
            "id": 1,
            "title": "TechStart Inc.",
            "category": "Business Website",
            "description": "Modern corporate website with advanced features",
            "technologies": ["React", "Node.js", "MongoDB"],
            "results": "40% increase in leads",
        },
        {
            "id": 2,
            "title": "Urban Fashion",
            "category": "E-commerce Store",
            "description": "Complete online store with payment integration",
            "technologies": ["Shopify", "React", "Stripe"],
            "results": "300% sales growth",
        },
        {
            "id": 3,
            "title": "GrowthCo Marketing",
            "category": "Landing Page",
            "description": "High-converting landing page for marketing agency",
            "technologies": ["Next.js", "Tailwind", "Analytics"],
            "results": "85% conversion rate",
        },
    ]
    return jsonify({"portfolio": portfolio_items}), 200


# Health check (Render probes this)
@app.get("/api/health")
def health_check():
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "HandleServ API",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now().isoformat(),
            }
        ),
        200,
    )


# ── Serve React/HTML front-end build from /static ─────────────────────────────
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    static_root = app.static_folder
    if not static_root:
        return "Static folder not configured", 404

    file_path = os.path.join(static_root, path)
    index_path = os.path.join(static_root, "index.html")

    if path and os.path.exists(file_path):
        return send_from_directory(static_root, path)
    if os.path.exists(index_path):
        return send_from_directory(static_root, "index.html")
    return "index.html not found", 404


# ── Dev server entry­point (ignored by Gunicorn in production) ────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
