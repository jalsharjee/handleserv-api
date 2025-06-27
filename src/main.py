import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
import datetime

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'handleserv#2024$secure'

# Enable CORS for all routes
CORS(app, origins="*")

app.register_blueprint(user_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Video Consultation API Routes
@app.route('/api/consultation/request', methods=['POST'])
def consultation_request():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'projectType', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Store consultation request (in a real app, save to database)
        consultation_data = {
            'id': f"CONS_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone', ''),
            'projectType': data['projectType'],
            'budget': data.get('budget', '$100'),
            'timeline': data.get('timeline', ''),
            'description': data['description'],
            'preferredTime': data.get('preferredTime', ''),
            'status': 'pending',
            'created_at': datetime.datetime.now().isoformat(),
            'price': '$100'
        }
        
        return jsonify({
            'success': True,
            'message': 'Consultation request received successfully!',
            'consultationId': consultation_data['id'],
            'data': consultation_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/consultation/developers', methods=['GET'])
def get_developers():
    developers = [
        {
            'id': 1,
            'name': 'Sarah Johnson',
            'specialty': 'Business Websites & E-commerce',
            'experience': '5+ years',
            'rating': 4.9,
            'projects': 150,
            'price': '$100',
            'available': True
        },
        {
            'id': 2,
            'name': 'Mike Chen',
            'specialty': 'Custom Web Applications',
            'experience': '7+ years',
            'rating': 4.8,
            'projects': 200,
            'price': '$100',
            'available': True
        },
        {
            'id': 3,
            'name': 'Lisa Rodriguez',
            'specialty': 'UI/UX Design & Development',
            'experience': '6+ years',
            'rating': 4.9,
            'projects': 180,
            'price': '$100',
            'available': True
        }
    ]
    
    return jsonify({'developers': developers}), 200

@app.route('/api/contact', methods=['POST'])
def contact_form():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Store contact message (in a real app, save to database)
        contact_data = {
            'id': f"MSG_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': data['name'],
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'],
            'status': 'new',
            'created_at': datetime.datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully! We will get back to you within 24 hours.',
            'messageId': contact_data['id']
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    portfolio_items = [
        {
            'id': 1,
            'title': 'TechStart Inc.',
            'category': 'Business Website',
            'description': 'Modern corporate website with advanced features',
            'technologies': ['React', 'Node.js', 'MongoDB'],
            'results': '40% increase in leads'
        },
        {
            'id': 2,
            'title': 'Urban Fashion',
            'category': 'E-commerce Store',
            'description': 'Complete online store with payment integration',
            'technologies': ['Shopify', 'React', 'Stripe'],
            'results': '300% sales growth'
        },
        {
            'id': 3,
            'title': 'GrowthCo Marketing',
            'category': 'Landing Page',
            'description': 'High-converting landing page for marketing agency',
            'technologies': ['Next.js', 'Tailwind', 'Analytics'],
            'results': '85% conversion rate'
        }
    ]
    
    return jsonify({'portfolio': portfolio_items}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'HandleServ API',
        'version': '1.0.0',
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

