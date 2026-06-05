TRUNCATE TABLE users;
TRUNCATE TABLE tasks;


ALTER SEQUENCE users_id_seq RESTART WITH 1;
ALTER SEQUENCE tasks_id_seq RESTART WITH 1;


INSERT INTO users (user_name, first_name, last_name, email, password_hash)
VALUES ('cookie_mons', 'Cookie', 'Monster', 'cookie@gmail.com', '$2b$10$rjX2FUd2Geu91ci6.NCloOwv/qLOHRSLUnIA0k72V6EwIBFNLJms.'),
       ('Bon','Porada', 'Thonglong', 'bonn@gmail.com', '$2b$10$rjX2FUd2Geu91ci6.NCloOwv/qLOHRSLUnIA0k72V6EwIBFNLJms.'),
       ('Justin', 'Justin', 'Kenealy', 'justin@gmail.com', '$2b$10$rjX2FUd2Geu91ci6.NCloOwv/qLOHRSLUnIA0k72V6EwIBFNLJms.'),
       ('Munsat', 'Munsat', 'Rukaya', 'munsat@gmail.com', '$2b$10$rjX2FUd2Geu91ci6.NCloOwv/qLOHRSLUnIA0k72V6EwIBFNLJms.'),
       ('Tania', 'Tania', 'Hosseini', 'tania@gmail.com', '$2b$10$rjX2FUd2Geu91ci6.NCloOwv/qLOHRSLUnIA0k72V6EwIBFNLJms.');


INSERT INTO tasks (user_id, name, description, creation_date, due_date, due_time, priority_level, status)
VALUES (1, 'Set up development environment', 'This task involves setting up the necessary software and tools required for the development of the project.', '2024-04-22', '2024-04-23', '10:00:00', 1, 1),
       (1, 'Design app wireframes', 'The goal of this task is to create wireframes for the user interface of the new mobile app.', '2024-04-23', '2024-04-25', '12:00:00', 2, 1),
       (1, 'Develop login functionality', 'This task involves creating a secure and user-friendly login system for the application.', '2024-04-25', '2024-04-27', '14:00:00', 3, 0),
       (1, 'Create dashboard page', 'This task involves designing and developing a dashboard page for the project.', '2024-04-27', '2024-04-30', '16:00:00', 4, 0),
       (2, 'Watch online tutorials', 'This will help get some knowledge on cooking', '2024-04-23', '2024-04-25', '10:00:00', 1, 1),
       (2, 'Buy ingredients', 'The list of ingredients includes vegetables, spices, meat.', '2024-04-26', '2024-04-28', '12:00:00', 2, 0),
       (2, 'Cook the dish', 'Make sure to follow food safety guidelines, use appropriate cooking techniques.', '2024-04-28', '2024-04-30', '14:00:00', 3, 0),
       (3, 'Review course material', 'write some notes', '2024-04-24', '2024-04-25', '16:00:00', 1, 1),
       (3, 'Complete all the Labs', 'tick off labs that have been completed', '2024-04-28', '2024-04-30', '18:00:00', 2, 0);

