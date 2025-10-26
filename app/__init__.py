import os
from flask import Flask
from .db import close_db, init_db_command
from .routes import bp as main_bp

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # Load config
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

    # Register CLI command (flask init-db)
    app.cli.add_command(init_db_command)

    return app
