from flask import request
from datetime import datetime
from app import app, db
from app.models import Post, User
from fake_data import post_data

@app.route('/')
def index():
    return 'Hello World'

# Get All Posts
@app.route('/posts')
def get_posts():
    posts = db.session.execute(db.select(Post).order_by(db.desc(Post.date_created))).scalars().all()
    return [post.to_dict() for post in posts]

# Get Post By ID
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get the post based on the post id
    post = db.session.get(Post, post_id)
    if post:
        return post.to_dict()
    else:
        return {'error': f'Post with {post_id} does not exist'}, 404

# Create New Post
@app.route('/posts', methods=['POST'])
def create_post():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    # Get data from the body
    title = data.get('title')
    body = data.get('body')

    # Create a new post
    new_post = Post(title=title, body=body, user_id=1)
    return new_post.to_dict(), 201

# Create new user
@app.route('/users', methods=['POST'])
def create_user():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    # Get the data from the request body
    data = request.json

    # Check to see if all of the required fiels are present
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    # Get the values from the data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check for already existing username or email 
    check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    if check_user:
        return {'error': 'A user with that username and/or email already exists'}, 400

    # Create a new user
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201
