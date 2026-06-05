DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  user_name VARCHAR(255) NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id INT,
          CONSTRAINT fk_tasks_users
          FOREIGN KEY(user_id)
          REFERENCES users(id)
          ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  creation_date DATE,
  due_date DATE, 
  due_time TIME,
  priority_level INT, 
  status INT
);
