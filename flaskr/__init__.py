"""
This script sets up a basic Flask application using the Factory Pattern.

Explanation:
------------
1. `import os` and `from flask import Flask`:
   - Import the `os` module for file path management and the Flask class to create the web app.

2. `def create_app(test_config=None):`
   - Defines a function that creates and configures the Flask application.
   - This pattern makes the app easier to configure and test.

3. `app = Flask(__name__, instance_relative_config=True)`:
   - Creates the Flask app.
   - `__name__` tells Flask where to find resources.
   - `instance_relative_config=True` allows the app to use a separate instance folder for configurations.

4. `app.config.from_mapping(...)`:
   - Sets up default configurations:
     - `SECRET_KEY='dev'`: Used for session security (should be overridden in production).
     - `DATABASE=...`: Defines the path to the SQLite database inside the instance folder.

5. `if test_config is None: ... else: ...`:
   - If `test_config` is not provided:
     - Load additional settings from `config.py` (if available).
   - If `test_config` is provided:
     - Override the app’s config with the test configuration (useful for unit testing).

6. `try: os.makedirs(app.instance_path)`:
   - Ensures the instance folder exists.
   - The instance folder stores configuration files and the database, kept outside version control.

7. `@app.route('/hello')`:
   - Defines a simple route `/hello` that returns `"Hello, World"` when accessed in the browser.

8. `from . import db` and `db.init_app(app)`:
   - Imports a database module and initializes it with the Flask app.
   - This binds database functions (like connection management) to the app.

9. `return app`:
   - Returns the fully configured Flask application instance.

Overall:
--------
This file demonstrates the recommended way of structuring a Flask project using the Application Factory Pattern.
It allows flexibility, easier testing, and better configuration management.
"""

import os
from flask import Flask

def create_app(test_config=None):
    # Create the Flask app instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Set default configuration values
    app.config.from_mapping(
        SECRET_KEY='dev',  # Secret key for session security (should be overridden in production)
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')  # Path to SQLite DB
    )

    # Load custom config if provided, otherwise fall back to config.py
    if test_config is None:
        # Load the instance config (if it exists)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Use test configuration (useful for testing environments)
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # If the folder already exists, ignore the error

    # Example route
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    # Import and initialize the database
    from . import db
    db.init_app(app)
    
    # Return the application instance
    return app
