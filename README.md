MiniBlog

MiniBlog is a desktop blogging application built with Python. It uses CustomTkinter for a modern GUI and MySQL as its database backend. Users can register/login, create, edit, and delete posts, and interact via comments and likes/dislikes. An admin role provides elevated privileges (e.g. managing all posts and users). This README provides an overview, setup instructions, and additional resources.

Key Features

User Accounts: Registration and login system with authentication.

Blog Posts: Create, edit, and delete blog posts through a GUI. Deleted posts go to a Recycle Bin for possible restoration.

Comments & Reactions: Users can comment on posts, and like or dislike posts.

Admin Panel: A special administrator role that can manage (view/delete) all posts and users.

Database-Backed: All data (users, posts, comments, likes) are stored in a MySQL database with a clear schema (see ER diagram below).

Technology Stack

Python 3.x: The core programming language. (Recommend Python 3.8 or later.)

CustomTkinter: A modern UI library based on Tkinter for the GUI
customtkinter.tomschimansky.com
. It provides customizable, consistent-looking widgets across Windows, macOS, and Linux.

MySQL: The relational database system for storing data. MySQL is the world’s most popular open-source database
mysql.com
, chosen for its reliability and performance.

MySQL Connector/Python: A Python library to connect with MySQL (you can use mysql-connector-python or PyMySQL).

Virtual Environment (optional): Recommended to isolate project dependencies
w3schools.com
.

Setup Instructions

Requirements: Ensure you have Python 3.x installed. Also install MySQL Community Server. Install required Python packages, for example:

pip install customtkinter mysql-connector-python


(CustomTkinter may require additional prerequisites depending on your OS.)

Virtual Environment (optional): It’s best to create an isolated environment to manage dependencies
w3schools.com
. For example:

python3 -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate


Database Setup:

Open MySQL and create a new database (e.g. miniblog).

Create the necessary tables. You can refer to the provided ER diagram (erd.png) for the schema. Alternatively, if a schema SQL file is included, import it into your database.

Update the database connection settings in the project (host, user, password, database name) as needed.

Running the App: Launch the application by running the main script. From the project directory:

python blog_gui.py


Ensure your virtual environment is active (if using one) and the MySQL server is running. The GUI should open, allowing you to register or log in and use MiniBlog.

ER Diagram

An Entity-Relationship (ER) diagram (erd.png) is included to illustrate the database schema. This diagram shows the blog database structure: entities (tables) like Users, Posts, Comments, etc., and their relationships
edrawmax.com
. ER diagrams are commonly used in requirements analysis to model the information to be stored in a database
edrawmax.com
. Refer to erd.png in the repository for details on tables and their relations.

File Structure

A simplified overview of the project files:

MiniBlog/
├─ blog_gui.py         # Main application (entry point)
├─ config.py           # (Optional) Configuration for DB connection
├─ models/             # (Optional) Data model classes (User, Post, Comment, etc.)
├─ views/              # (Optional) GUI screens (login, home, post editor)
├─ database.py         # (Optional) Database helper functions
├─ erd.png             # Entity-Relationship diagram for the database
└─ README.md           # Project documentation (this file)


Adjust the above structure to match the actual project layout. Each module and folder contains code relevant to its purpose (e.g. models/ for data classes, views/ for GUI code).

Author

This project was developed by the MiniBlog team. For questions or feedback, you can contact the author or open an issue on the project’s repository.

References: This application uses CustomTkinter for the GUI
customtkinter.tomschimansky.com
 and relies on MySQL as the database
mysql.com
. The provided ER diagram follows standard design principles
