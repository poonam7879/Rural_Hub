import os

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    
    # Database config
    # Vercel / Neon / Supabase uses DATABASE_URL
    # Ensure we use postgresql:// instead of postgres:// for SQLAlchemy 1.4+
    if os.environ.get('VERCEL'):
        default_db = 'sqlite:////tmp/local_dev.db'
    else:
        default_db = 'sqlite:///local_dev.db'
        
    db_url = os.environ.get('DATABASE_URL', default_db)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cloudinary Config
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
