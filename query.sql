INSERT INTO user_info(first_name,last_name,email,contact,bio,user_name)
VALUES()

------INSERT DATA 
INSERT INTO user_info (first_name, last_name, email, contact, user_name, bio) VALUES
('John', 'Doe', 'john@example.com', '01710000001', 'johndoe', 'Tech blogger'),
('Alice', 'Smith', 'alice@example.com', '01710000002', 'alicesmith', 'Food enthusiast'),
('Bob', 'Johnson', 'bob@example.com', '01710000003', 'bobjohnson', 'Travel blogger'),
('Carol', 'Davis', 'carol@example.com', '01710000004', 'caroldavis', 'Lifestyle writer'),
('David', 'Miller', 'david@example.com', '01710000005', 'davidm', 'Photography fan'),
('Eva', 'Wilson', 'eva@example.com', '01710000006', 'evawilson', 'Fitness trainer'),
('Frank', 'Moore', 'frank@example.com', '01710000007', 'frankmoore', 'Music lover'),
('Grace', 'Taylor', 'grace@example.com', '01710000008', 'gracetaylor', 'Movie critic'),
('Henry', 'Anderson', 'henry@example.com', '01710000009', 'henryand', 'Gaming geek'),
('Isla', 'Thomas', 'isla@example.com', '01710000010', 'islathomas', 'Fashion blogger');
-------|>
INSERT INTO user_pass (user_id, password) VALUES
(1, '

'),
(2, 'password2'),
(3, 'password3'),
(4, 'password4'),
(5, 'password5'),
(6, 'password6'),
(7, 'password7'),
(8, 'password8'),
(9, 'password9'),
(10, 'password10');
-------|>
INSERT INTO blog (title, main_blog, created_by) VALUES
('Tech Trends 2025', 'Content about AI and ML...', 1),
('Healthy Recipes', 'Content about healthy meals...', 2),
('Travel Diaries: Japan', 'Content about Tokyo...', 3),
('Morning Routine Tips', 'Content about productivity...', 4),
('Photography 101', 'Content about camera basics...', 5),
('Fitness Challenge', 'Content about workouts...', 6),
('Top 10 Songs', 'Content about music...', 7),
('Movie Review: Inception', 'Content about the movie...', 8),
('Gaming Tips', 'Content about gaming...', 9),
('Fashion Trends', 'Content about fashion...', 10),
('AI in Daily Life', 'Content about AI tools...', 1),
('Vegan Recipes', 'Content about vegan meals...', 2),
('Backpacking Europe', 'Content about Europe travel...', 3),
('Work From Home Setup', 'Content about productivity...', 4),
('Portrait Photography', 'Content about lighting...', 5),
('Home Workout', 'Content about exercises...', 6),
('Top Albums 2025', 'Content about albums...', 7),
('Movie Review: Avatar', 'Content about the movie...', 8),
('Esports Tournaments', 'Content about gaming events...', 9),
('Street Fashion', 'Content about city fashion...', 10),
('Cloud Computing Basics', 'Content about cloud...', 1),
('Gluten-Free Recipes', 'Content about recipes...', 2),
('Hiking Trails', 'Content about mountains...', 3),
('Time Management', 'Content about productivity...', 4),
('Landscape Photography', 'Content about landscapes...', 5),
('Yoga at Home', 'Content about yoga...', 6),
('Concert Review', 'Content about concerts...', 7),
('Movie Review: Matrix', 'Content about the movie...', 8),
('Gaming Gear', 'Content about accessories...', 9),
('Seasonal Fashion', 'Content about fashion...', 10);
--------|>
INSERT INTO blog_comments (blog_id, user_id, comment_text) VALUES
(1, 2, 'Great insights on AI!'),
(2, 3, 'I love these recipes!'),
(3, 1, 'Japan looks amazing!'),
(4, 5, 'Very helpful tips!'),
(5, 6, 'Photography is fun!'),
(6, 7, 'Challenge accepted!'),
(7, 8, 'Nice music selection!'),
(8, 9, 'Loved the review!'),
(9, 10, 'Helpful gaming tips!'),
(10, 1, 'Fashion trends are awesome!');
--------|>

INSERT INTO blog_reactions (blog_id, user_id, reaction) VALUES
(1, 2, 'like'),
(2, 3, 'like'),
(3, 1, 'like'),
(4, 5, 'dislike'),
(5, 6, 'like'),
(6, 7, 'dislike'),
(7, 8, 'like'),
(8, 9, 'like'),
(9, 10, 'like'),
(10, 1, 'dislike');
-------|> query for functions
INSERT INTO user_info (first_name, last_name, contact, email, bio, user_name)
VALUES (first_name, last_name, contact, email, bio, user_name)

INSERT INTO user_pass (user_id, password)
VALUES (u_id, password)

SELECT id, first_name, last_name, email, contact, bio, user_name, created_at
FROM user_info
WHERE id = "self._user_id"

SELECT u.id AS user_id, u.user_name, p.password 
FROM user_info u
JOIN user_pass p ON u.id = p.user_id
WHERE u.user_name = "user_name"

INSERT INTO blog (title, main_blog, created_by)
VALUES (title, main_blog, "self._user_id")

SELECT b.*, u.user_name, u.first_name, u.last_name
FROM blog b
LEFT JOIN user_info u ON b.created_by = u.id
WHERE b.dlt = 0
ORDER BY b.created_at DESC

SELECT * FROM blog 
WHERE created_by=self._user_id AND dlt=0 ORDER BY created_at DESC

SELECT
SUM(CASE WHEN created_by = self._user_id AND dlt = 0 THEN 1 ELSE 0 END) AS active,
SUM(CASE WHEN created_by = self._user_idAND dlt = 1 THEN 1 ELSE 0 END) AS trashed,
SUM(CASE WHEN dlt = 0 THEN 1 ELSE 0 END) AS community
FROM blog