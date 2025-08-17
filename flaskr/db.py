"""
This file handles all database-related operations for the Flask application.

Explanation:
------------
1. `import sqlite3` and `from datetime import datetime`:
   - `sqlite3`: Provides a lightweight SQL database engine.
   - `datetime`: Helps convert database timestamps into Python datetime objects.

2. `import click`:
   - Used to create custom Flask CLI (command-line interface) commands.

3. `from flask import current_app, g`:
   - `current_app`: Gives access to the active Flask application.
   - `g`: A special object for storing data during a request (per-request storage).

Functions:
----------
1. `get_db()`:
   - Opens a database connection if not already open for the current request.
   - Uses `sqlite3.connect` with `detect_types=sqlite3.PARSE_DECLTYPES` to automatically convert database types.
   - Sets `row_factory` to `sqlite3.Row`, so results behave like dictionaries (easier to work with).

2. `close_db(e=None)`:
   - Closes the database connection at the end of the request.
   - Called automatically by Flask’s `teardown_appcontext`.

3. `init_db()`:
   - Initializes the database by running SQL statements from `schema.sql`.

4. `init_db_command()`:
   - Defines a CLI command (`flask init-db`).
   - Clears existing data and recreates tables by calling `init_db()`.
   - Prints a confirmation message.

5. `sqlite3.register_converter("timestamp", ...)`:
   - Ensures that SQLite timestamp fields are automatically converted into Python `datetime` objects.

6. `init_app(app)`:
   - Registers `close_db` to run after each request (`teardown`).
   - Adds the custom CLI command `init-db` to the Flask app.

Overall:
--------
This file centralizes all database logic for the Flask app.
It ensures:
- Each request has its own database connection.
- Connections are cleaned up automatically.
- The app can easily be initialized/reset with a CLI command.
"""

import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
