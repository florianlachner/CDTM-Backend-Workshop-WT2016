PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Lists;
-- TODO: Create Table Lists here
CREATE TABlE Lists(
  id         INTEGER     PRIMARY KEY Autoincrement,
  title      TEXT        NOT NULL,
  revision   INTEGER     NOT NULL DEFAULT '1',
  inbox      INTEGER     NOT NULL DEFAULT '0',
  created    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS Tasks;
-- TODO: Create Table Tasks here
CREATE TABlE Tasks(
  id          INTEGER     PRIMARY KEY Autoincrement,
  list        INTEGER     NOT NULL,
  title       TEXT        NOT NULL,
  status      TEXT        NOT NULL,
  description TEXT        NOT NULL,
  due         TIMESTAMP   NOT NULL,
  revision    INTEGER     NOT NULL DEFAULT '1',
  created     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);