# Report
## Twitter from Temu - A Social Network Service

### Idea
We wanted to create a social networking service inspired by the older version of Twitter (now X). We brainstormed for a suitable name and ended up with the name "Cheeper", playing on the bird sounds of "cheep cheep" and the idea of anything Chinese being "cheaper".

### fastAPI
We decided to go for fastAPI as web-framework for the API serving the back-end functionality of the application.

#### Endpoints

GET / — Read Root: Shows a message: "Server is running"

POST /signup/ — Signup: Handles signups from front end through an authorization route

POST /login/ — Login: Authenticates a user logging in through an authorization route

---

GET /users/ — Read Users: Retrieves a list of users.

POST /users/ — Add User: Adds a new user.

GET /users/{user_id} — Read User: Retrieves data for a specific user by ID.

PUT /users/{user_id} — Update User: Fully updates a specific user (replace all data).

PATCH /users/{user_id} — Patch User: Partially updates a user (e.g., just a name or email).

DELETE /users/{user_id} — Delete User: Deletes a user.

---

GET /posts/ — Get All Posts: Retrieves all posts.

POST /posts/ — Create Post: Adds a new post.

GET /posts/{post_id} — Get Post: Retrieves a specific post by ID.

PUT /posts/{post_id} — Update Post: Fully updates a specific post.

PATCH /posts/{post_id} — Patch Post: Partially updates a post.

DELETE /posts/{post_id} — Delete Post: Removes a post.

![fastAPI docs.](/images/fastAPI.jpg")

### mySQL hosted on Clever Cloud

We decided to use mySQL as a relational database hosted on Clever Cloud (a free PaaS).
Cheeper has their own organization page on the service with each developer accessing the databse through seperate logins.

#### Databse credentials

Each developer has database credentials saved in an .env for local testing. Credentials are encrypted with dotenv for security purposes, but db credentials are also stored in Render for server deployment.

![Database configuration.](/images/db-config.jpg")

#### SQLAlchemy
We decided to implement the use of SQLAlchemy in our API to ensure cleaner code and more secure queries. This allows for python code, instead of having to write raw SQL queries.

![SQLAlchemy import for db schemas.](/images/sqlalchemy.jpg")

SQLAlchemy also simplifies database access by establishing a database connection through a create_engine function that provides connection with the database.

![SQLAlchemy import for db schemas.](/images/sqlalchemy-engine.jpg")

### Render
The API is deployed on Render on https://idg2001-o1-social-networking-service.onrender.com/

### User authorization
We decided to implement password hashing by using bcrypt for user safety and to prevent cyber attacks.

### Caching
Local caching is provided..

### Frontend
We used a simple, yet moder design for our frontend using HTML, CSS and JavaScript. The logo is inspired by the old twitter logo and is an outline of a Sparrow, as Sparrows' sounds are "cheep cheep". 


