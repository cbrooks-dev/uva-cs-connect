import os
from flask import Flask, request, abort, Response
from .db import close_db, init_db_command
from .routes import bp as main_bp
from .add import bp as add_bp

def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='templates',
        static_folder='static',
        static_url_path='/static'
    )

    # Basic configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),  # use environment variable if available
        SESSION_COOKIE_HTTPONLY=True,   # prevents JavaScript from accessing session cookie
        SESSION_COOKIE_SECURE=False,    # set to True in production with HTTPS
        SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register teardown (closes DB connection after each request)
    app.teardown_appcontext(close_db)

    # Register the main blueprint (routes)
    app.register_blueprint(main_bp)
    app.register_blueprint(add_bp)

    # Register CLI command (flask init-db)
    app.cli.add_command(init_db_command)

    # ----- Basic Security Measures -----
    @app.before_request
    def limit_request_size():
        # Reject requests over 2 MB
        max_size = 2 * 1024 * 1024
        if request.content_length and request.content_length > max_size:
            abort(413)  # Payload Too Large

    @app.after_request
    def set_security_headers(response: Response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Basic XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
