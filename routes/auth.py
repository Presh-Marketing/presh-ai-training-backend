from flask import Blueprint, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from src.models.training import db, User, LearningActivity
import os
import os
import secrets

auth_bp = Blueprint('auth', __name__)

# OAuth configuration
oauth = OAuth()

# Allowed email domain (configurable via env)
ALLOWED_DOMAIN = os.getenv('ALLOWED_DOMAIN', 'presh.ai')

def init_oauth(app):
    oauth.init_app(app)
    
    # Google OAuth configuration
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret'),
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    return google

def is_authorized_domain(email):
    """Check if email belongs to authorized domain"""
    return email.lower().endswith(f'@{ALLOWED_DOMAIN}')

@auth_bp.route('/login', methods=['GET'])
def login():
    """Initiate Google OAuth login"""
    google = oauth.google
    
    # Generate a random state parameter for security
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Redirect to Google OAuth
    # Ensure callback uses the frontend origin so session cookies bind to the frontend domain
    frontend_origin = os.getenv('FRONTEND_ORIGIN')
    if frontend_origin:
        redirect_uri = frontend_origin.rstrip('/') + url_for('auth.callback')
    else:
        redirect_uri = url_for('auth.callback', _external=True)
    return google.authorize_redirect(redirect_uri, state=state)

@auth_bp.route('/callback', methods=['GET'])
def callback():
    """Handle Google OAuth callback"""
    google = oauth.google
    
    # Verify state parameter
    if request.args.get('state') != session.get('oauth_state'):
        return redirect('/?error=invalid_state')
    
    try:
        # Get access token
        token = google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            user_info = google.parse_id_token(token)
        
        # Check domain authorization
        user_email = user_info['email']
        if not is_authorized_domain(user_email):
            return redirect(f'/?error=unauthorized_domain&domain={ALLOWED_DOMAIN}')
        
        # Check if user exists
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            # Create new user
            user = User(
                name=user_info.get('name', user_email),
                email=user_email,
                role='Marketing Strategist'
            )
            db.session.add(user)
            db.session.commit()
            
            # Log enrollment activity
            activity = LearningActivity(
                user_id=user.id,
                activity_type='enrollment',
                description='Joined AI Solution Designer Program via Google OAuth'
            )
            db.session.add(activity)
            db.session.commit()
        
        # Store user in session
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.name
        
        # Redirect to dashboard
        return redirect('/')
        
    except Exception as e:
        return redirect(f'/?error=auth_failed&message={str(e)}')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Log out the current user"""
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/user', methods=['GET'])
def get_current_user():
    """Get current authenticated user"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'progress': {
            'currentTrack': user.current_track,
            'currentModule': user.current_module,
            'completedModules': user.get_completed_modules(),
            'certifications': user.get_certifications()
        }
    })

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    user_id = session.get('user_id')
    return jsonify({
        'authenticated': user_id is not None,
        'user_id': user_id,
        'user_name': session.get('user_name'),
        'user_email': session.get('user_email')
    })

# Middleware to require authentication
def require_auth():
    """Decorator to require authentication for routes"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

