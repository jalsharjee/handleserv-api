from flask import Blueprint, request, jsonify
from src.models.user import db
import datetime

orders_bp = Blueprint('orders', __name__)

# Mock data for demonstration
orders_data = []

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    
    new_order = {
        'id': len(orders_data) + 1,
        'client_name': data.get('client_name'),
        'client_email': data.get('client_email'),
        'package': data.get('package'),
        'project_type': data.get('project_type'),
        'requirements': data.get('requirements'),
        'deadline': data.get('deadline'),
        'price': data.get('price'),
        'status': 'Pending Payment',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    orders_data.append(new_order)
    
    return jsonify({
        'success': True,
        'message': 'Order created successfully',
        'order': new_order
    }), 201

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify({
        'success': True,
        'orders': orders_data
    })

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order"""
    for order in orders_data:
        if order['id'] == order_id:
            return jsonify({
                'success': True,
                'order': order
            })
    
    return jsonify({
        'success': False,
        'message': 'Order not found'
    }), 404

@orders_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    data = request.get_json()
    
    for order in orders_data:
        if order['id'] == order_id:
            order['status'] = data.get('status')
            return jsonify({
                'success': True,
                'message': 'Order status updated successfully',
                'order': order
            })
    
    return jsonify({
        'success': False,
        'message': 'Order not found'
    }), 404

@orders_bp.route('/packages', methods=['GET'])
def get_packages():
    """Get available packages"""
    packages = [
        {
            'name': 'Starter',
            'price': 299,
            'description': 'Perfect for small businesses and personal websites',
            'features': [
                'Up to 5 pages',
                'Mobile responsive design',
                'Basic SEO optimization',
                'Contact form integration',
                '7-day delivery',
                '1 revision round'
            ]
        },
        {
            'name': 'Professional',
            'price': 599,
            'description': 'Ideal for growing businesses and e-commerce',
            'features': [
                'Up to 10 pages',
                'Custom design & branding',
                'Advanced SEO optimization',
                'E-commerce integration',
                'Social media integration',
                '14-day delivery',
                '3 revision rounds',
                '30-day support'
            ]
        },
        {
            'name': 'Enterprise',
            'price': 999,
            'description': 'Complete solution for large businesses',
            'features': [
                'Unlimited pages',
                'Premium custom design',
                'Advanced functionality',
                'Database integration',
                'Third-party API integration',
                '21-day delivery',
                'Unlimited revisions',
                '90-day support',
                'Performance optimization'
            ]
        }
    ]
    
    return jsonify({
        'success': True,
        'packages': packages
    })

