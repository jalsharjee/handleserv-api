from flask import Blueprint, request, jsonify
from src.models.user import db
import datetime

projects_bp = Blueprint('projects', __name__)

# Mock data for demonstration
projects_data = [
    {
        'id': 1,
        'client_name': 'John Doe',
        'project_type': 'Business Website',
        'status': 'In Progress',
        'deadline': '2025-06-20',
        'freelancer': 'Alice Smith',
        'price': 599
    },
    {
        'id': 2,
        'client_name': 'Jane Wilson',
        'project_type': 'E-commerce Site',
        'status': 'Completed',
        'deadline': '2025-06-15',
        'freelancer': 'Bob Johnson',
        'price': 999
    }
]

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    return jsonify({
        'success': True,
        'projects': projects_data
    })

@projects_bp.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    new_project = {
        'id': len(projects_data) + 1,
        'client_name': data.get('client_name'),
        'project_type': data.get('project_type'),
        'status': 'Pending',
        'deadline': data.get('deadline'),
        'freelancer': None,
        'price': data.get('price')
    }
    
    projects_data.append(new_project)
    
    return jsonify({
        'success': True,
        'message': 'Project created successfully',
        'project': new_project
    }), 201

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update project status"""
    data = request.get_json()
    
    for project in projects_data:
        if project['id'] == project_id:
            project.update(data)
            return jsonify({
                'success': True,
                'message': 'Project updated successfully',
                'project': project
            })
    
    return jsonify({
        'success': False,
        'message': 'Project not found'
    }), 404

@projects_bp.route('/projects/<int:project_id>/assign', methods=['POST'])
def assign_freelancer(project_id):
    """Assign freelancer to project"""
    data = request.get_json()
    
    for project in projects_data:
        if project['id'] == project_id:
            project['freelancer'] = data.get('freelancer')
            project['status'] = 'Assigned'
            return jsonify({
                'success': True,
                'message': 'Freelancer assigned successfully',
                'project': project
            })
    
    return jsonify({
        'success': False,
        'message': 'Project not found'
    }), 404

