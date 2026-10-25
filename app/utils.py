import os
from functools import wraps
from urllib.parse import urlparse

from flask import abort, current_app
from flask_login import current_user
import cloudinary
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
    if not file or not getattr(file, 'filename', None):
        return None

    filename = file.filename.lower()
    allowed_exts = ('.jpg', '.jpeg', '.png', '.webp')
    if not filename.endswith(allowed_exts):
        return None

    try:
        cloudinary_url = current_app.config.get('CLOUDINARY_URL') or os.getenv('CLOUDINARY_URL')
        if cloudinary_url:
            parsed = urlparse(cloudinary_url)
            if parsed.scheme == 'cloudinary' and parsed.hostname:
                cloudinary.config(
                    cloud_name=parsed.hostname,
                    api_key=parsed.username,
                    api_secret=parsed.password,
                )

        config = cloudinary.config()
        if not getattr(config, 'api_key', None):
            print('Cloudinary is not configured. Missing api_key.')
            return None

        if hasattr(file, 'stream'):
            file.stream.seek(0)

        upload_result = cloudinary.uploader.upload(
            file,
            resource_type='image',
            folder='rural_hub',
            allowed_formats=['jpg', 'jpeg', 'png', 'webp']
        )
        return upload_result.get('secure_url')
    except Exception as e:
        print(f"Image upload error: {e}")
        return None
