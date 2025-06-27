from flask import Blueprint, request, jsonify
from src.models.user import db
import datetime
import uuid

affiliate_bp = Blueprint('affiliate', __name__)

# Mock affiliate database
affiliates = [
    {
        'id': 1,
        'name': 'John Marketing',
        'email': 'john@marketing.com',
        'affiliate_code': 'JOHN2025',
        'commission_rate': 0.15,
        'total_earnings': 1250.00,
        'total_referrals': 8,
        'status': 'active',
        'joined_date': '2025-01-15'
    },
    {
        'id': 2,
        'name': 'Sarah Business',
        'email': 'sarah@business.com',
        'affiliate_code': 'SARAH15',
        'commission_rate': 0.15,
        'total_earnings': 890.50,
        'total_referrals': 5,
        'status': 'active',
        'joined_date': '2025-02-01'
    }
]

# Mock referral tracking
referrals = [
    {
        'id': 1,
        'affiliate_id': 1,
        'customer_email': 'customer1@example.com',
        'order_value': 599.00,
        'commission_earned': 89.85,
        'status': 'paid',
        'date': '2025-06-01'
    },
    {
        'id': 2,
        'affiliate_id': 1,
        'customer_email': 'customer2@example.com',
        'order_value': 299.00,
        'commission_earned': 44.85,
        'status': 'pending',
        'date': '2025-06-10'
    }
]

@affiliate_bp.route('/affiliate/register', methods=['POST'])
def register_affiliate():
    """Register a new affiliate"""
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({
            'success': False,
            'message': 'Name and email are required'
        }), 400
    
    # Check if email already exists
    existing_affiliate = next((a for a in affiliates if a['email'] == email), None)
    if existing_affiliate:
        return jsonify({
            'success': False,
            'message': 'Email already registered as affiliate'
        }), 400
    
    # Generate unique affiliate code
    affiliate_code = f"{name.upper().replace(' ', '')[:5]}{len(affiliates) + 1}"
    
    new_affiliate = {
        'id': len(affiliates) + 1,
        'name': name,
        'email': email,
        'affiliate_code': affiliate_code,
        'commission_rate': 0.15,  # 15% commission
        'total_earnings': 0.00,
        'total_referrals': 0,
        'status': 'active',
        'joined_date': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    
    affiliates.append(new_affiliate)
    
    return jsonify({
        'success': True,
        'message': 'Affiliate registration successful',
        'affiliate': new_affiliate
    })

@affiliate_bp.route('/affiliate/dashboard/<affiliate_code>', methods=['GET'])
def get_affiliate_dashboard(affiliate_code):
    """Get affiliate dashboard data"""
    affiliate = next((a for a in affiliates if a['affiliate_code'] == affiliate_code), None)
    
    if not affiliate:
        return jsonify({
            'success': False,
            'message': 'Affiliate not found'
        }), 404
    
    # Get affiliate's referrals
    affiliate_referrals = [r for r in referrals if r['affiliate_id'] == affiliate['id']]
    
    # Calculate statistics
    total_clicks = len(affiliate_referrals) * 5  # Mock click data
    conversion_rate = (len(affiliate_referrals) / max(total_clicks, 1)) * 100
    pending_earnings = sum(r['commission_earned'] for r in affiliate_referrals if r['status'] == 'pending')
    
    dashboard_data = {
        'affiliate_info': affiliate,
        'statistics': {
            'total_clicks': total_clicks,
            'total_referrals': len(affiliate_referrals),
            'conversion_rate': round(conversion_rate, 2),
            'total_earnings': affiliate['total_earnings'],
            'pending_earnings': pending_earnings
        },
        'recent_referrals': affiliate_referrals[-5:],  # Last 5 referrals
        'referral_link': f"https://wcugjzce.manus.space?ref={affiliate_code}"
    }
    
    return jsonify({
        'success': True,
        'dashboard': dashboard_data
    })

@affiliate_bp.route('/affiliate/track-referral', methods=['POST'])
def track_referral():
    """Track a new referral"""
    data = request.get_json()
    
    affiliate_code = data.get('affiliate_code')
    customer_email = data.get('customer_email')
    order_value = data.get('order_value', 0)
    
    if not affiliate_code or not customer_email:
        return jsonify({
            'success': False,
            'message': 'Affiliate code and customer email are required'
        }), 400
    
    # Find affiliate
    affiliate = next((a for a in affiliates if a['affiliate_code'] == affiliate_code), None)
    if not affiliate:
        return jsonify({
            'success': False,
            'message': 'Invalid affiliate code'
        }), 404
    
    # Calculate commission
    commission_earned = order_value * affiliate['commission_rate']
    
    # Create new referral record
    new_referral = {
        'id': len(referrals) + 1,
        'affiliate_id': affiliate['id'],
        'customer_email': customer_email,
        'order_value': order_value,
        'commission_earned': commission_earned,
        'status': 'pending',
        'date': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    
    referrals.append(new_referral)
    
    # Update affiliate stats
    affiliate['total_referrals'] += 1
    
    return jsonify({
        'success': True,
        'message': 'Referral tracked successfully',
        'referral': new_referral
    })

@affiliate_bp.route('/affiliate/validate-code/<affiliate_code>', methods=['GET'])
def validate_affiliate_code(affiliate_code):
    """Validate affiliate code and return affiliate info"""
    affiliate = next((a for a in affiliates if a['affiliate_code'] == affiliate_code), None)
    
    if not affiliate:
        return jsonify({
            'success': False,
            'message': 'Invalid affiliate code'
        }), 404
    
    return jsonify({
        'success': True,
        'affiliate': {
            'name': affiliate['name'],
            'code': affiliate['affiliate_code'],
            'commission_rate': affiliate['commission_rate']
        }
    })

@affiliate_bp.route('/affiliate/generate-links', methods=['POST'])
def generate_affiliate_links():
    """Generate marketing materials and links for affiliate"""
    data = request.get_json()
    affiliate_code = data.get('affiliate_code')
    
    affiliate = next((a for a in affiliates if a['affiliate_code'] == affiliate_code), None)
    if not affiliate:
        return jsonify({
            'success': False,
            'message': 'Invalid affiliate code'
        }), 404
    
    base_url = "https://wcugjzce.manus.space"
    
    marketing_materials = {
        'referral_links': {
            'homepage': f"{base_url}?ref={affiliate_code}",
            'starter_package': f"{base_url}?ref={affiliate_code}&package=starter",
            'professional_package': f"{base_url}?ref={affiliate_code}&package=professional",
            'enterprise_package': f"{base_url}?ref={affiliate_code}&package=enterprise"
        },
        'email_templates': [
            {
                'subject': 'Get Your Professional Website Built - 15% Off!',
                'body': f"Hi there! I wanted to share an amazing service I found for professional website design. WebCraft Pro creates stunning websites with a 30% faster turnaround than traditional agencies. Use my referral link to get started: {base_url}?ref={affiliate_code}"
            },
            {
                'subject': 'Transform Your Business with a Professional Website',
                'body': f"Looking to establish a strong online presence? WebCraft Pro offers complete website solutions starting at just $299. They handle everything from design to deployment. Check them out: {base_url}?ref={affiliate_code}"
            }
        ],
        'social_media_posts': [
            f"🚀 Need a professional website for your business? WebCraft Pro delivers amazing results with automated workflows and quality guarantees! Check them out: {base_url}?ref={affiliate_code} #WebDesign #Business",
            f"💼 Just discovered WebCraft Pro - they create professional websites 60% faster than traditional agencies! Perfect for entrepreneurs and small businesses: {base_url}?ref={affiliate_code}",
            f"✨ WebCraft Pro makes professional web design accessible to everyone. Three packages starting at $299. Quality guaranteed! {base_url}?ref={affiliate_code} #WebDevelopment"
        ],
        'banner_codes': [
            f'<a href="{base_url}?ref={affiliate_code}"><img src="https://via.placeholder.com/728x90/4F46E5/FFFFFF?text=WebCraft+Pro+-+Professional+Websites" alt="WebCraft Pro"></a>',
            f'<a href="{base_url}?ref={affiliate_code}"><img src="https://via.placeholder.com/300x250/4F46E5/FFFFFF?text=Get+Your+Website+Built" alt="WebCraft Pro"></a>'
        ]
    }
    
    return jsonify({
        'success': True,
        'marketing_materials': marketing_materials
    })

@affiliate_bp.route('/affiliate/payment-history/<affiliate_code>', methods=['GET'])
def get_payment_history(affiliate_code):
    """Get affiliate payment history"""
    affiliate = next((a for a in affiliates if a['affiliate_code'] == affiliate_code), None)
    if not affiliate:
        return jsonify({
            'success': False,
            'message': 'Invalid affiliate code'
        }), 404
    
    # Mock payment history
    payment_history = [
        {
            'id': 1,
            'amount': 450.00,
            'date': '2025-05-01',
            'status': 'paid',
            'method': 'PayPal',
            'referrals_count': 3
        },
        {
            'id': 2,
            'amount': 800.00,
            'date': '2025-04-01',
            'status': 'paid',
            'method': 'Bank Transfer',
            'referrals_count': 5
        }
    ]
    
    return jsonify({
        'success': True,
        'payment_history': payment_history
    })

@affiliate_bp.route('/affiliate/leaderboard', methods=['GET'])
def get_affiliate_leaderboard():
    """Get top performing affiliates"""
    # Sort affiliates by total earnings
    top_affiliates = sorted(affiliates, key=lambda x: x['total_earnings'], reverse=True)[:10]
    
    leaderboard = []
    for i, affiliate in enumerate(top_affiliates):
        leaderboard.append({
            'rank': i + 1,
            'name': affiliate['name'],
            'total_earnings': affiliate['total_earnings'],
            'total_referrals': affiliate['total_referrals']
        })
    
    return jsonify({
        'success': True,
        'leaderboard': leaderboard
    })

@affiliate_bp.route('/affiliate/all', methods=['GET'])
def get_all_affiliates():
    """Get all affiliates (admin endpoint)"""
    return jsonify({
        'success': True,
        'affiliates': affiliates
    })

