/*
==================================================
Flask Blog Application - Database Schema
==================================================

This SQL script initializes the database for the Flask
application. It defines two main tables: `user` and `post`.

1. DROP TABLE IF EXISTS:
   - Ensures old tables (`user`, `post`) are removed
     before creating fresh ones. This avoids conflicts
     when re-initializing the database.

2. CREATE TABLE user:
   - Columns:
     - id: Primary key, auto-incremented integer.
     - username: Unique username, cannot be NULL.
     - password: User’s password (hashed in practice).

3. CREATE TABLE post:
   - Columns:
     - id: Primary key, auto-incremented integer.
     - author_id: Foreign key referencing `user.id`,
       ensures each post is tied to a valid user.
     - created: Timestamp of creation, defaults to
       current time.
     - title: Title of the blog post.
     - body: Content of the blog post.
   - Foreign Key: `author_id` links each post to its author.

Usage:
-------
- This schema is executed when initializing the database
  using the Flask CLI command: `flask init-db`.
- It creates a simple blog structure with users and posts.

==================================================
*/

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
