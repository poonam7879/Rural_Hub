from urllib.parse import urlparse

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import create_engine, text
import cloudinary
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if db_uri and db_uri.startswith('postgresql://'):
        try:
            engine = create_engine(db_uri, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text('SELECT 1'))
        except Exception:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_dev.db'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    if app.config.get('CLOUDINARY_URL'):
        parsed = urlparse(app.config['CLOUDINARY_URL'])
        if parsed.scheme == 'cloudinary' and parsed.hostname:
            cloudinary.config(
                cloud_name=parsed.hostname,
                api_key=parsed.username,
                api_secret=parsed.password,
            )

    # Import parts of our application
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.scrap import scrap
    from app.routes.services import services
    from app.routes.barter import barter
    from app.routes.dashboards import dashboards
    from app.routes.admin import admin

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(scrap, url_prefix='/scrap')
    app.register_blueprint(services, url_prefix='/services')
    app.register_blueprint(barter, url_prefix='/barter')
    app.register_blueprint(dashboards, url_prefix='/dashboard')
    app.register_blueprint(admin, url_prefix='/admin')

    # Global error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('main/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import render_template
        return render_template('main/500.html'), 500

    @app.errorhandler(401)
    def unauthorized(e):
        from flask import render_template
        return render_template('main/401.html'), 401

    return app
