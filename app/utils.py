import os
from functools import wraps
from flask import abort, current_app
from flask_login import current_user
import cloudinary.uploader

def role_required(role):
    """
    Decorator to restrict access to a specific role.
    Role can be a string or list of strings.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            roles = [role] if isinstance(role, str) else role
            if current_user.role not in roles and current_user.role != 'admin':
                abort(403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def upload_image(file):
    """
    Uploads an image to Cloudinary and returns the secure URL.
    Returns None if upload fails or no file is provided.
    """
    if not file:
        return None
        
    try:
        # Vercel filesystem is read-only, but Cloudinary Python SDK 
        # can accept a FileStorage object directly (buffered in memory).
        upload_result = cloudinary.uploader.upload(file)
        return upload_result.get('secure_url')
    except Exception as e:
        print(f"Image upload error: {e}")
        return None
