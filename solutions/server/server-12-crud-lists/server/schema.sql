PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
  id          INTEGER      PRIMARY KEY AUTOINCREMENT,
  email       TEXT         NOT NULL UNIQUE,
  password    TEXT         NOT NULL,
  created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS Lists;
CREATE TABLE Lists(
    id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    title       TEXT         NOT NULL,
    revision    INTEGER      NOT NULL DEFAULT 1,
    inbox       INTEGER      NOT NULL DEFAULT 0,
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
  );

DROP TABLE IF EXISTS Collaborators;
CREATE TABLE Collaborators(
  user_id          INTEGER      NOT NULL,
  list_id          INTEGER      NOT NULL,
  PRIMARY KEY (user_id, list_id),
  FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE,
  FOREIGN KEY(list_id ) REFERENCES Lists(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Tasks;
CREATE TABLE Tasks(
    id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    list        INTEGER      NOT NULL,
    title       TEXT         NOT NULL,
    status      TEXT         NOT NULL,
    description TEXT         NOT NULL DEFAULT '',
    due         TIMESTAMP    ,
    revision    INTEGER      NOT NULL DEFAULT 1,
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(list) REFERENCES Lists(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Uploads;
CREATE TABLE Uploads(
  task        INTEGER      NOT NULL,
  filename    TEXT         NOT NULL,
  created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (task, filename),
  FOREIGN KEY(task) REFERENCES Tasks(id) ON DELETE CASCADE
);

INSERT INTO Lists (title, revision, inbox) VALUES ('Inbox', 1, 1);
