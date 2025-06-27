from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid

consultation_bp = Blueprint('consultation', __name__)

# Sample developer data (in production, this would be in a database)
developers = [
    {
        "id": 1,
        "name": "Sarah Johnson",
        "email": "sarah@handleserv.com",
        "specialty": "Business Websites & E-commerce",
        "rating": 4.9,
        "experience": "5+ years",
        "calendly_link": "https://calendly.com/sarah-handleserv",
        "zoom_room": "https://zoom.us/j/1234567890",
        "availability": ["2025-01-20", "2025-01-21", "2025-01-22"],
        "time_slots": ["09:00", "11:00", "14:00", "16:00"]
    },
    {
        "id": 2,
        "name": "Mike Chen",
        "email": "mike@handleserv.com",
        "specialty": "React & Modern Web Apps",
        "rating": 4.8,
        "experience": "7+ years",
        "calendly_link": "https://calendly.com/mike-handleserv",
        "zoom_room": "https://zoom.us/j/0987654321",
        "availability": ["2025-01-20", "2025-01-23", "2025-01-24"],
        "time_slots": ["10:00", "13:00", "15:00", "17:00"]
    },
    {
        "id": 3,
        "name": "Lisa Rodriguez",
        "email": "lisa@handleserv.com",
        "specialty": "UI/UX Design & Development",
        "rating": 5.0,
        "experience": "6+ years",
        "calendly_link": "https://calendly.com/lisa-handleserv",
        "zoom_room": "https://zoom.us/j/1122334455",
        "availability": ["2025-01-21", "2025-01-22", "2025-01-25"],
        "time_slots": ["09:30", "12:00", "14:30", "16:30"]
    }
]

# In-memory storage for consultations (use database in production)
consultations = []

@consultation_bp.route('/developers', methods=['GET'])
def get_developers():
    """Get list of available developers"""
    return jsonify({
        "success": True,
        "developers": developers
    })

@consultation_bp.route('/book', methods=['POST'])
def book_consultation():
    """Book a video consultation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['package', 'developer', 'date', 'time', 'client']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Validate client information
        client = data['client']
        if not client.get('name') or not client.get('email'):
            return jsonify({
                "success": False,
                "error": "Client name and email are required"
            }), 400
        
        # Find the developer
        developer = next((d for d in developers if d['id'] == data['developer']), None)
        if not developer:
            return jsonify({
                "success": False,
                "error": "Developer not found"
            }), 404
        
        # Check availability
        if data['date'] not in developer['availability']:
            return jsonify({
                "success": False,
                "error": "Developer not available on selected date"
            }), 400
        
        if data['time'] not in developer['time_slots']:
            return jsonify({
                "success": False,
                "error": "Time slot not available"
            }), 400
        
        # Generate consultation ID
        consultation_id = str(uuid.uuid4())
        
        # Create consultation record
        consultation = {
            "id": consultation_id,
            "package": data['package'],
            "developer_id": data['developer'],
            "developer_name": developer['name'],
            "developer_email": developer['email'],
            "date": data['date'],
            "time": data['time'],
            "client": client,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "zoom_link": developer['zoom_room'],
            "calendly_link": developer['calendly_link']
        }
        
        consultations.append(consultation)
        
        # In production, you would:
        # 1. Send confirmation email to client
        # 2. Send notification to developer
        # 3. Create calendar events
        # 4. Set up automated reminders
        
        return jsonify({
            "success": True,
            "consultation_id": consultation_id,
            "message": "Consultation booked successfully",
            "details": {
                "developer": developer['name'],
                "date": data['date'],
                "time": data['time'],
                "zoom_link": developer['zoom_room']
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@consultation_bp.route('/consultations', methods=['GET'])
def get_consultations():
    """Get all consultations (admin endpoint)"""
    return jsonify({
        "success": True,
        "consultations": consultations
    })

@consultation_bp.route('/consultations/<consultation_id>', methods=['GET'])
def get_consultation(consultation_id):
    """Get specific consultation details"""
    consultation = next((c for c in consultations if c['id'] == consultation_id), None)
    
    if not consultation:
        return jsonify({
            "success": False,
            "error": "Consultation not found"
        }), 404
    
    return jsonify({
        "success": True,
        "consultation": consultation
    })

@consultation_bp.route('/consultations/<consultation_id>/status', methods=['PUT'])
def update_consultation_status(consultation_id):
    """Update consultation status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['scheduled', 'in_progress', 'completed', 'cancelled']:
            return jsonify({
                "success": False,
                "error": "Invalid status"
            }), 400
        
        consultation = next((c for c in consultations if c['id'] == consultation_id), None)
        
        if not consultation:
            return jsonify({
                "success": False,
                "error": "Consultation not found"
            }), 404
        
        consultation['status'] = new_status
        consultation['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            "success": True,
            "message": "Status updated successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@consultation_bp.route('/developers/<int:developer_id>/availability', methods=['GET'])
def get_developer_availability(developer_id):
    """Get specific developer's availability"""
    developer = next((d for d in developers if d['id'] == developer_id), None)
    
    if not developer:
        return jsonify({
            "success": False,
            "error": "Developer not found"
        }), 404
    
    return jsonify({
        "success": True,
        "availability": {
            "dates": developer['availability'],
            "time_slots": developer['time_slots']
        }
    })

# Email notification function (placeholder)
def send_consultation_confirmation(consultation):
    """Send confirmation email to client and developer"""
    # In production, integrate with email service like SendGrid
    print(f"Sending confirmation email for consultation {consultation['id']}")
    
    # Email to client
    client_email_content = f"""
    Dear {consultation['client']['name']},
    
    Your video consultation has been confirmed!
    
    Details:
    - Developer: {consultation['developer_name']}
    - Date: {consultation['date']}
    - Time: {consultation['time']}
    - Zoom Link: {consultation['zoom_link']}
    
    Please join the call 5 minutes early.
    
    Best regards,
    HandleServ Team
    """
    
    # Email to developer
    developer_email_content = f"""
    Hi {consultation['developer_name']},
    
    You have a new consultation scheduled:
    
    Client: {consultation['client']['name']} ({consultation['client']['email']})
    Date: {consultation['date']}
    Time: {consultation['time']}
    Package: {consultation['package']}
    Project Description: {consultation['client'].get('projectDescription', 'Not provided')}
    
    Zoom Link: {consultation['zoom_link']}
    
    Please prepare for the consultation and join on time.
    
    Best regards,
    HandleServ Team
    """
    
    return True

