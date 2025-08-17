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

8. `return app`:
   - Returns the fully configured Flask application instance.

Overall:
--------
This file demonstrates the recommended way of structuring a Flask project using the Application Factory Pattern.
It allows flexibility, easier testing, and better configuration management.
"""

import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    return app
