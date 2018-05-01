DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
  id integer PRIMARY KEY AUTOINCREMENT,
  title text NOT NULL,
  'text' text NOT NULL
);


-- This schema consists of a single table called entries.
-- Each row in this table has an id, a title, and a text.
-- The id is an automatically incrementing integer and a primary key,
-- the other two are strings that must not be null.