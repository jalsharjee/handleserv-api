# src/routes/projects.py
from flask import Blueprint, jsonify

projects_bp = Blueprint("projects", __name__, url_prefix="/api/projects")

@projects_bp.get("/")
def list_projects():
    # placeholder response; replace with real DB lookup later
    return jsonify([]), 200
