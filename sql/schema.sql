PRAGMA foreign_keys = ON;

/*TODO: IS EVERYTHING SUPPOSED TO BE NOT NULL*/
CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(username)
);

CREATE TABLE posts(
  postid INTEGER NOT NULL,
  filename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(postid),
  FOREIGN KEY (owner) REFERENCES users (username) ON DELETE CASCADE
);


CREATE TABLE following(
  username1 varchar(20) NOT NULL,
  username2 varchar(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (username1) REFERENCES users (username) ON DELETE CASCADE,
  FOREIGN KEY (username2) REFERENCES users (username) ON DELETE CASCADE,
  PRIMARY KEY (username1, username2)
);

CREATE TABLE comments(
  commentid INTEGER NOT NULL,
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  text VARCHAR(1024) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (commentid),
  FOREIGN KEY (owner) REFERENCES users (username) ON DELETE CASCADE,
  FOREIGN KEY (postid) REFERENCES posts (postid) ON DELETE CASCADE
);

CREATE TABLE likes(
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (owner, postid),
  FOREIGN KEY (owner) REFERENCES users (username) ON DELETE CASCADE,
  FOREIGN KEY (postid) REFERENCES posts (postid) ON DELETE CASCADE
);