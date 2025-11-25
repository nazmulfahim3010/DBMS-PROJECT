CREATE DATABASE IF NOT EXISTS miniblog2;
USE miniblog2;

CREATE TABLE user_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contact VARCHAR(50) NOT NULL,
    bio TEXT,
    user_name VARCHAR(150) NOT NULL UNIQUE,
    
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_pass (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    
    -- bcrypt hash (always binary)
    password VARBINARY(255) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES user_info(id)
        ON DELETE CASCADE
);

CREATE TABLE blog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    main_blog TEXT NOT NULL,
    created_by INT NOT NULL,
    
    dlt TINYINT(1) DEFAULT 0, -- soft delete flag
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by) REFERENCES user_info(id)
        ON DELETE CASCADE
);

CREATE TABLE blog_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blog_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (blog_id) REFERENCES blog(id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_info(id)
        ON DELETE CASCADE
);



CREATE TABLE blog_reactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blog_id INT NOT NULL,
    user_id INT NOT NULL,
    
    reaction ENUM('like', 'dislike') NOT NULL,
    
    UNIQUE KEY unique_react (blog_id, user_id),
    FOREIGN KEY (blog_id) REFERENCES blog(id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_info(id)
        ON DELETE CASCADE
);

